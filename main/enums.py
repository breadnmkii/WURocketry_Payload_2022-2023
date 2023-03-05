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
    # John
    pass

class Deployed(Enum):
    # Logan
    pass

class System_Flags(Enum):
    STAGE_INFO = (Stage.PRELAUNCH, Stage.MIDAIR, Stage.LANDED)
    MOVEMENT = (Movement.NOT_MOVING, Movement.MOVING, Movement.CONFLICTING_DECISION)
    FLIGHT_DIRECTION = (Flight_Direction.MOVING_UP, Flight_Direction.MOVING_DOWN, Flight_Direction.INDETERMINENT)
    VERTICALITY = (Verticality.NOT_UPRIGHT, Verticality.UPRIGHT)
    # John
    SEPARATED = None
    # Logan
    DEPLOYED = None

    def __init__(self, STAGE_INFO, MOVEMENT, FLIGHT_DIRECTION,  VERTICALITY, SEPARATED, DEPLOYED):
        self.STAGE_INFO = STAGE_INFO
        self.MOVEMENT = MOVEMENT
        self.FLIGHT_DIRECTION = FLIGHT_DIRECTION
        self.VERTICALITY = VERTICALITY
        self.SEPARATED = SEPARATED
        self.DEPLOYED = DEPLOYED