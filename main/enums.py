from enum import Enum, IntEnum

class Stage(IntEnum):
    PRELAUNCH = 0
    MIDAIR = 1
    LANDED = 2

class Movement(IntEnum):
    NOT_MOVING = 0
    MOVING = 1
    CONFLICTING_DECISION = 2

class Flight_Direction(IntEnum):
    MOVING_UP = 0
    MOVING_DOWN = 1
    INDETERMINENT = 2

class Verticality(IntEnum):
    NOT_UPRIGHT = 0
    UPRIGHT = 1

class Separated(IntEnum):
    NOT_SEPARATED = 0
    SEPARATED = 1

class Deployed(IntEnum):
    NOT_DEPLOYED = 0
    DEPLOYED = 1

class Warn_Heat(IntEnum):
    NOMINAL = 0
    WARNING = 1

class Warn_Camera(IntEnum):
    NOMINAL = 0
    WARNING = 1

class Warn_Avionics(IntEnum):
    NOMINAL = 0
    WARNING_BNO = 1
    WARNING_BMP = 2
    WARNING_SYS = 3 # entire system (both bno and bmp warning)

class Warn_Motive(IntEnum):
    NOMINAL = 0
    WARNING = 1

class System_Flags():
    # STAGE_INFO = (Stage.PRELAUNCH, Stage.MIDAIR, Stage.LANDED)
    # MOVEMENT = (Movement.NOT_MOVING, Movement.MOVING, Movement.CONFLICTING_DECISION)
    # FLIGHT_DIRECTION = (Flight_Direction.MOVING_UP, Flight_Direction.MOVING_DOWN, Flight_Direction.INDETERMINENT)
    # VERTICALITY = (Verticality.NOT_UPRIGHT, Verticality.UPRIGHT)
    # SEPARATED = (Separated.SEPARATED, Separated.NOT_SEPARATED)
    # DEPLOYED = (Deployed.DEPLOYED, Deployed.NOT_DEPLOYED)
    # WARN_HEAT = (Warn_Heat.NOMINAL, Warn_Heat.WARNING)
    # WARN_CAMERA = (Warn_Camera.NOMINAL, Warn_Camera.WARNING)
    # WARN_AVIONICS = (Warn_Avionics.NOMINAL, Warn_Avionics.WARNING_BMP, Warn_Avionics.WARNING_BNO, Warn_Avionics.WARNING_SYS)
    # WARN_MOTIVE = (Warn_Motive.NOMINAL, Warn_Motive.WARNING)

    def __init__(self, STAGE_INFO, MOVEMENT, FLIGHT_DIRECTION, VERTICALITY, SEPARATED, DEPLOYED, HEAT, CAMERA_MODULE, AVIONICS, MOTIVE):
        self.STAGE_INFO = STAGE_INFO
        self.MOVEMENT = MOVEMENT
        self.FLIGHT_DIRECTION = FLIGHT_DIRECTION
        self.VERTICALITY = VERTICALITY
        self.SEPARATED = SEPARATED
        self.DEPLOYED = DEPLOYED
        self.WARN_HEAT = HEAT
        self.WARN_CAMERA = CAMERA_MODULE
        self.WARN_AVIONICS = AVIONICS 
        self.WARN_MOTIVE = MOTIVE
    
    def get_str(self):
        flags = (str(self.STAGE_INFO), str(self.MOVEMENT), str(self.FLIGHT_DIRECTION), str(self.VERTICALITY), str(self.SEPARATED), str(self.DEPLOYED), str(self.WARN_HEAT), str(self.WARN_CAMERA), str(self.WARN_AVIONICS), str(self.WARN_MOTIVE))
        return flags
    
    def get_int(self):
        flags = (int(self.STAGE_INFO), int(self.MOVEMENT), int(self.FLIGHT_DIRECTION), int(self.VERTICALITY), int(self.SEPARATED), int(self.DEPLOYED), int(self.WARN_HEAT), int(self.WARN_CAMERA), int(self.WARN_AVIONICS), int(self.WARN_MOTIVE))
        return flags

    def get_bitmask_str(self):
        flags = self.get_int()
        bitmask_str = ""
        for flag in flags:
            bitmask_str += str(flag)
        return bitmask_str