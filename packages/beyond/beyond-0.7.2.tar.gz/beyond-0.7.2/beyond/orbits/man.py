import logging
import numpy as np
from abc import ABCMeta, abstractmethod

from ..frames.local import to_local, to_tnw

log = logging.getLogger(__name__)


class Man(metaclass=ABCMeta):
    """Abstract Maneuver class"""

    @abstractmethod
    def check(self):
        pass


class ImpulsiveMan(Man):
    """Impulsive maneuver"""

    def __init__(self, date, dv, frame=None, comment=None):
        """
        Args:
            date (Date): Date of application of the maneuver
            dv (list): Vector of length 3 describing the velocity increment
            frame (str): Which frame is used for applying the increment : ``'TNW'``,
                ``'QSW'`` or ``None``. If ``frame = None`` the same frame as
                the orbit is used
            comment (str): Free text to give context on a given maneuver
                ('apogee maneuver', 'inclination correction')
        """

        if len(dv) != 3:
            raise ValueError("dv should be 3 in length")

        if isinstance(frame, str):
            frame = frame.upper()

        self.date = date
        self._dv = np.array(dv)
        self.frame = frame
        self.comment = comment

    def __repr__(self):  # pragma: no cover
        txt = "Man =\n  date = {}\n".format(self.date)
        if self.frame:
            txt += "  frame = {}\n".format(self.frame)
        if self.comment:
            txt += "  comment = {}\n".format(self.comment)
        txt += "  dv = \n"
        for i, x in enumerate("xyz"):
            txt += "    {} = {:0.2g} m/s\n".format(x, self._dv[i])
        return txt

    def check(self, date, step):
        return date < self.date <= date + step

    def dv(self, orb, **kwargs):
        """Computation of the velocity increment in the reference frame of the orbit

        Args:
            orb (Orbit):
        Return:
            numpy.array: Velocity increment, length 3
        """

        orb = orb.copy(form="cartesian")

        if self.frame in ("QSW", "TNW"):
            mat = to_local(self.frame, orb, expanded=False).T
        else:
            mat = np.identity(3)

        # velocity increment in the same reference frame as the orbit
        projected_dv = mat @ self._dv

        return projected_dv


class KeplerianImpulsiveMan(ImpulsiveMan):
    """Impulsive maneuver directly modifying keplerian parameters changes

    For maximum efficiency:

    * 'a' should be modified at apoapsis or periapsis, via delta_a
    * 'i' should be modified at descending or ascending node, via delta_angle
    * 'Ω' should be modified at argument of latitude +/- 90 deg, via delta_angle
    """

    def __init__(self, date, *, delta_a=0, delta_angle=0, comment=None):
        """
        Args:
            date (Date): Date of application of the impulsive maneuver
            delta_a (float): Semi major axis increment
            delta_angle (float): inclination or right ascention of ascending node increment (radians)
            comment (str):
        """
        self.date = date
        self.delta_a = delta_a
        self.delta_angle = delta_angle
        self.comment = comment

    def __repr__(self):  # pragma: no cover
        txt = "Man =\n  date = {}\n".format(self.date)
        if self.delta_a:
            txt += "  delta_a = {} m\n".format(self.delta_a)
        if self.delta_angle:
            txt += "  delta_angle = {} rad\n".format(self.delta_angle)
        if self.comment:
            txt += "  comment = {}\n".format(self.comment)
        return txt

    def dv(self, orb, **kwargs):
        self._dv = dkep2dv(orb, delta_a=self.delta_a, delta_angle=self.delta_angle)

        return to_tnw(orb).T @ self._dv


class ContinuousMan(Man):
    """Continuous thrust"""

    def __init__(
        self,
        date,
        duration,
        *,
        dv=None,
        accel=None,
        date_pos="start",
        frame=None,
        comment=None
    ):
        """
        Args:
            date (Date): Date (see date_pos)
            duration (timedelta): Duration of the thrust
            dv (list[float]): Vector of length 3 describing the velocity increment (in m/s)
            accel (list[float]): Vector of length 3 describing the acceleration (in m/s²)
            date_pos (str): define the position of the date argument. Accepted values are ``start``, ``stop``, ``median``
            frame (str): frame of the maneuver
            comment (str):
        """
        if date_pos.lower() not in ["start", "stop", "median"]:
            raise ValueError("date_pos accepted values are start, stop and median")
        if isinstance(frame, str):
            frame = frame.upper()
        if frame in ("RSW", "LVLH", "QSW"):
            frame = "QSW"

        self.date = date
        self.duration = duration
        self.date_pos = date_pos.lower()

        if self.date_pos == "start":
            self.start = date
        elif self.date_pos == "median":
            self.start = date - duration / 2
        else:
            self.start = date - duration

        self.stop = self.start + duration
        self.median = self.start + duration / 2

        if accel is None and dv is None:
            raise ValueError("One of dv or accel should be filled")
        elif accel is not None and dv is not None:
            raise ValueError("Only one of dv or accel should be filled")
        elif dv is not None and len(dv) != 3:
            raise ValueError("dv should be 3 in length")
        elif dv is not None:
            self._dv = np.array(dv)
            self._accel = self._dv / self.duration.total_seconds()
        elif len(accel) != 3:
            raise ValueError("accel should be 3 in length")
        else:
            self._accel = np.array(accel)
            self._dv = self._accel * self.duration.total_seconds()

        self.frame = frame
        self.comment = comment

        log.debug("Man [{}; {}[".format(self.start, self.stop))

    def __repr__(self):  # pragma: no cover
        txt = """ContinuousMan =
  start    = {0.start}
  stop     = {0.stop}
  median   = {0.median}
  duration = {0.duration}
"""
        if self.frame:
            txt += "  frame    = {0.frame}\n"
        if self.comment:
            txt += "  comment  = {0.comment}\n"
        txt += "  dv\n"
        for i, x in enumerate("xyz"):
            txt += "    {} = {:0.2g} m/s²\n".format(x, self._accel[i])
        return txt.format(self)

    def check(self, date):
        return self.start <= date < self.stop

    def accel(self, orb):

        orb = orb.copy(form="cartesian")

        if self.frame in ("QSW", "TNW"):
            mat = to_local(self.frame, orb, expanded=False).T
        else:
            mat = np.identity(3)

        projected_accel = mat @ self._accel

        log.debug(
            "{} accel_{}={} accel_{}={} norm={}".format(
                orb.date,
                self.frame,
                self._accel.tolist(),
                orb.propagator.frame,
                projected_accel.tolist(),
                np.linalg.norm(self._accel),
            )
        )

        return projected_accel


class KeplerianContinuousMan(ContinuousMan):
    def __init__(self, date, duration, **kwargs):
        kwargs["frame"] = "TNW"
        self.delta_a = kwargs.pop("delta_a", 0)
        self.delta_angle = kwargs.pop("delta_i", 0)
        super().__init__(date, duration, np.zeros(3), **kwargs)

    def accel(self, orb):
        self._dv = dkep2dv(orb, delta_a=self.delta_a, delta_angle=self.delta_angle)
        return super().accel(orb)


def dkep2dv(orb, *, delta_a=0, delta_angle=0):
    """Convert a increment in keplerian elements to a delta v in TNW"""
    dv_a = orb.frame.center.body.mu * delta_a / (2 * orb.infos.v * orb.infos.kep.a ** 2)

    v_final = orb.infos.v + dv_a

    # Al-Kashi
    dv = np.sqrt(
        orb.infos.v ** 2
        + v_final ** 2
        - 2 * orb.infos.v * v_final * np.cos(delta_angle)
    )
    dv_t = v_final * np.cos(delta_angle) - orb.infos.v

    ratio = abs(dv_t / dv)

    # Due to some floating point operation rounding, this ratio
    # can be superior to one.
    if np.isclose(ratio, 1):
        dv_w = 0
    else:
        # equivalent to dv_w = dv * np.sin(np.arccos(ratio))
        dv_w = dv * np.sqrt(1 - ratio ** 2)

    return np.array([dv_t, 0, dv_w])
