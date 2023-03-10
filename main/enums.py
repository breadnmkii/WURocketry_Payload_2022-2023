from enum import Enum

class Stage(Enum):
    PRELAUNCH = 0
    MIDAIR = 1
    LANDED = 2

class Movement(Enum):
    NOT_MOVING = 0
    MOVING = 1
    CONFLICTING_DECISION = 2

class Flight_Direction(Enum):
    MOVING_UP = 0
    MOVING_DOWN = 1
    INDETERMINENT = 2

class Verticality(Enum):
    NOT_UPRIGHT = 0
    UPRIGHT = 1

class Separated(Enum):
    NOT_SEPARATED = 0
    SEPARATED = 1

class Deployed(Enum):
    NOT_DEPLOYED = 0
    DEPLOYED = 1

class Warn_Heat(Enum):
    NORMAL = 0
    WARNING = 1

class Warn_Camera(Enum):
    NORMAL = 0
    WARNING = 1


class Warn_Avionics(Enum):
    NORMAL = 0
    WARNING = 1

class Warn_Motive(Enum):
    # Logan
    pass


class System_Flags(Enum):
    STAGE_INFO = (Stage.PRELAUNCH, Stage.MIDAIR, Stage.LANDED)
    MOVEMENT = (Movement.NOT_MOVING, Movement.MOVING, Movement.CONFLICTING_DECISION)
    FLIGHT_DIRECTION = (Flight_Direction.MOVING_UP, Flight_Direction.MOVING_DOWN, Flight_Direction.INDETERMINENT)
    VERTICALITY = (Verticality.NOT_UPRIGHT, Verticality.UPRIGHT)
    # John
    SEPARATED = (Separated.SEPARATED, Separated.NOT_SEPARATED)
    # Logan
    DEPLOYED = (Deployed.DEPLOYED, Deployed.NOT_DEPLOYED)

    WARN_HEAT = (Warn_Heat.NORMAL, Warn_Heat.WARNING_HEAT)
    WARN_CAMERA = (Warn_Camera.NORMAL, Warn_Camera.WARNING_CAMERA)
    WARN_AVIONICS = (Warn_Avionics.NORMAL, Warn_Avionics.WARNING_BMP, Warn_Avionics.WARNING_BNO)
    # Logan
    WARN_MOTIVE = None

    def __init__(self, STAGE_INFO, MOVEMENT, FLIGHT_DIRECTION, VERTICALITY, SEPARATED, DEPLOYED, HEAT, CAMERA_MODULE, AVIONICS, MOTIVE):
        self.STAGE_INFO = STAGE_INFO
        self.MOVEMENT = MOVEMENT
        self.FLIGHT_DIRECTION = FLIGHT_DIRECTION
        self.VERTICALITY = VERTICALITY
        # John
        self.SEPARATED = SEPARATED
        # Logan
        self.DEPLOYED = DEPLOYED
        self.WARN_HEAT = HEAT
        self.WARN_CAMERA = CAMERA_MODULE
        self.WARN_AVIONICS = AVIONICS 
        # Logan
        self.WARN_MOTIVE = MOTIVE
