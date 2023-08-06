from typing import Optional, List, Union
from hein_robots.robotics import Location, Twist, Wrench, Cartesian, Orientation, Units
from hein_robots.base.actuators import Actuator
from hein_robots.base.grippers import Gripper


class RobotArm:
    @property
    def connected(self) -> bool:
        return False
    
    @property
    def max_velocity(self) -> float:
        return 0.0

    @max_velocity.setter
    def max_velocity(self, value: float):
        pass

    @property
    def max_acceleration(self) -> float:
        return 0.0

    @max_acceleration.setter
    def max_acceleration(self, value: float):
        pass

    @property
    def default_velocity(self) -> float:
        return 0.0

    @default_velocity.setter
    def default_velocity(self, value: float):
        pass

    @property
    def default_acceleration(self) -> float:
        return 0.0

    @default_acceleration.setter
    def default_acceleration(self, value: float):
        pass

    @property
    def acceleration(self) -> float:
        return 0.0

    @property
    def velocity(self) -> float:
        return 0.0

    @property
    def location(self) -> Location:
        return Location()

    @property
    def twist(self) -> Twist:
        return Twist()

    @property
    def wrench(self) -> Wrench:
        return Wrench()

    @property
    def joint_positions(self) -> List[float]:
        return []

    @property
    def joint_count(self) -> int:
        return 0

    def connect(self):
        pass

    def disconnect(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def emergency_stop(self):
        pass

    def clear_faults(self):
        pass

    def home(self, wait: bool = True):
        pass

    def move(self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None,
             rx: Optional[float] = None, ry: Optional[float] = None, rz: Optional[float] = None,
             velocity: Optional[float] = None, acceleration: Optional[float] = None,
             relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_to_location(self, location: Location,
                         velocity: Optional[float] = None, acceleration: Optional[float] = None,
                         relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_to_locations(self, *locations: Location,
                          velocity: Optional[float] = None, acceleration: Optional[float] = None,
                          relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_joints(self, *actuator_positions: float,
                       velocity: Optional[float] = None, acceleration: Optional[float] = None,
                       relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_joint(self, actuator_id: int, position: float,
                      velocity: Optional[float] = None, acceleration: Optional[float] = None,
                      relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_twist(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0,
                   duration: Optional[float] = None, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_twist_to(self, twist: Twist, duration: Optional[float] = None, wait: bool = True, timeout: Optional[float] = None):
        pass

    def open_gripper(self, position: Optional[Union[float, bool]] = None):
        pass

    def close_gripper(self, position: Optional[Union[float, bool]] = None):
        pass


class RobotArmError(Exception):
    pass


class RobotArmUnitsError(RobotArmError):
    pass


class RobotArmMovementError(RobotArmError):
    pass
