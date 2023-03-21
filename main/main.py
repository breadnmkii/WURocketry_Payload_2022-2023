# FILE FOR MAIN PAYLOAD MISSION ROUTINE

## Imports
#from Avionics import config as avionics_config
#from Imaging import config as imaging_config
#from Motive import config as motive_config

#from Avionics import sensing
from Control import fsm
#from Motive import camarm
from Radio import APRS
#from Radio import telemetry

import time
from enums import *


## Globals -- look into enums/dictionary for this 
'''
SYS ARRAY: [isMoving, hitApogee, hasDeployed]
sys_flags index 0: stage information, index 1: movement_decision, index 2: altitude_status
at index 0: 0 means prelaunch standby stage, 1 means payload midair, 2 means payload landed
at index 1: 0 means not moving, 1 means moving, 2 conflicting decisions
at index 2: 0 means moving up, 1 means moving down, 2 indeterminant 
at index 3: 0 means not upright, 1 means vertical position for camera
at index 6: 1 means BMP senses averaged temperature above 83 Celcius
at index 7: 1 means PiCamera initialization fails -- hardware fualt
at index 8: 1 means BNO or BMP initialization fails -- hardware fualt
IS UPRIGHT    index 3
IS SEPARATED  index 4
IS DEPLOYED   index 5
WARN HEAT     index 6
WARN CAMERA   index 7
WARN AVIONIC  index 8
WARN MOTIVE   index 9
'''
sys_flags = []
sys_flags = System_Flags(Stage.PRELAUNCH, Movement.NOT_MOVING, Flight_Direction.INDETERMINENT, Verticality.NOT_UPRIGHT, 
                         Separated.value, Deployed.value,
                         Warn_Heat.NORMAL, Warn_Camera.NORMAL, Warn_Avionics.NORMAL,
                         Warn_Motive.value)

'''
from enum import Enum
class System_Flags(Enum):
    STAGE_INFO = 0
    MOVMENT = 1
    DIRECTION = 2
    VERTICALITY = 3
    SEPARTED = 4
    DEPLOYED = 5
    WARN_HEAT = 6
    WARN_CAMERA = 7
    WARN_AVIONICS = 8
    WAR_MOTIVE = 9

'''




def updateRAFCO():
    imageCommands = []
    with open("data") as file:
        data = file.readlines()

        for line in data:
            cleanLine = line.strip("\n,;").split(" ")
            cleanLine = list(filter(None, cleanLine))
            imageCommands.append(cleanLine)
        file.close()
    
    return imageCommands




# Payload mission functions (base on payload mission execution flowchart??)
def avionicRoutine():
    # TODO: confirm design decision, add comments
    #acceleration_accumulator = []
    # initialize values
    has_launched = None # sensing.detectMovement(acc_accumulator) # true means movement detected, false means movement not detected
    is_still = None # sensing.remain_still(acc_accumulator) # true means still, false means not still
    # initialize values 
    is_upright = None
    heat = None
    bmp_values_status = None # sensing.altitude_status(altitude_accumulator, pressure_accumulator)
    ground_steady = None

    ### PRE-LAUNCH STANDBY ###
    if(sys_flags.STAGE_INFO == Stage.PRELAUNCH):
        (has_launched, is_still) = avionics_prelaunch()
    elif (sys_flags.STAGE_INFO == Stage.MIDAIR):
        # sample for movement (if launched)
        (has_launched, heat, is_still, ground_steady, bmp_values_status) = avionics_midair()
    elif (sys_flags.STAGE_INFO == Stage.LANDED):
        # check for no movement (if landed)
        # check for upright (orientation sensor)
        (heat, is_still, is_upright) = avionics_landed()

    # update system flags -- specifics (related to avionics)
    update_system_flags(is_upright,heat, bmp_values_status, has_launched, is_still, ground_steady)

def avionics_prelaunch():
    acceleration_buffer = sensing.read_acceleration_buffer()
    has_launched = sensing.detectMovement(acceleration_buffer)
    is_still = sensing.remain_still(acceleration_buffer)
    return (has_launched, is_still)

def avionics_midair():
    acceleration_buffer = sensing.read_acceleration_buffer()
    has_launched = sensing.detectMovement(acceleration_buffer)
    (temperature_buffer, pressure_buffer, altitude_buffer) = sensing.read_bmp()
    bmp_values_status = sensing.altitude_status(altitude_buffer, pressure_buffer)
    heat = sensing.check_heat(temperature_buffer)
    is_still = sensing.remain_still(acceleration_buffer)
    ground_steady = sensing.ground_level(altitude_buffer, pressure_buffer)
    return (has_launched, heat, is_still, ground_steady, bmp_values_status)

def avionics_landed():
    euler_buffer = sensing.read_euler_buffer()
    acceleration_buffer = sensing.read_acceleration_buffer()
    (temperature_buffer, pressure_buffer, altitude_buffer) = sensing.read_bmp()
    heat = sensing.check_heat(temperature_buffer)
    is_still = sensing.remain_still(acceleration_buffer)
    is_upright = sensing.vertical(euler_buffer)
    return (heat, is_still, is_upright)

def update_system_flags(is_upright,heat, bmp_values_status, has_launched, is_still, ground_steady):
    if is_upright:
        #sys_flags[3] = int(is_upright == True) 
        sys_flags.VERTICALITY = int(is_upright == True) 
    if heat:
        #sys_flags[6]  = int(heat == True) 
        sys_flags.WARN_HEAT = int(heat == True) 
    if bmp_values_status:
        # sys_flags[1] == 1
        if sys_flags.MOVEMENT == Movement.MOVING and bmp_values_status == 'up':
            #sys_flags[2] = 0     
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.MOVING_UP
        elif sys_flags.MOVEMENT == Movement.MOVING and bmp_values_status == 'down':
            #sys_flags[2] = 1
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.MOVING_DOWN
        else:
            #sys_flags[2] = 2
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.INDETERMINENT

    if has_launched and is_still:
        if has_launched and not is_still:
            #sys_flags[1] = 1
            sys_flags.MOVEMENT = Movement.MOVING
        elif not has_launched and  is_still:
            #sys_flags[1] = 0
            sys_flags.MOVEMENT = Movement.NOT_MOVING
        else:
            #sys_flags[1] = 2
            sys_flags.MOVEMENT = Movement.CONFLICTING_DECISION
            print('ATTENTION: linear acceleration and quarternion info not enough to determine the presence/absence of movement ')
    # Update sys flags
    # switch stages
    if (sys_flags.STAGE_INFO == Stage.PRELAUNCH and has_launched and bmp_values_status == 'up'):
        #stage = 2
        sys_flags.STAGE_INFO = Stage.MIDAIR
    if (sys_flags.STAGE_INFO == Stage.MIDAIR and is_still and ground_steady):
        #stage = 3
        sys_flags.STAGE_INFO = Stage.LANDED


HALF_SEPARATION_TIME = 10
def deployRoutine(motor, solenoids):
    if (sys_flags.STAGE_INFO == 3):
        if (sys_flags.DEPLOYED == Deployed.NOT_DEPLOYED):
            ##### REALIGN (New phase, need to "pull" nosecone back a bit to release retention)

            motor.throttle = -1
            time.sleep(0.5)
            motor.throttle = 0
            
            ##### RETENTION RELEASE PHASE
            while (sys_flags.MOVEMENT == Movement.MOVING): #The soleonid will not retract in if it detects movement
                continue

            # Retract all solenoids in retention
            for solenoid in solenoids:
                solenoid.throttle = 1

            while (sys_flags.MOVEMENT == Movement.MOVING): #Wait to transition from retracting retention to separation phase
                continue
                
            ##### SEPARATION PHASE
            motor.throttle = 1 #Motorhat will separate forward by half once it's not moving
            time.sleep(HALF_SEPARATION_TIME) 
            motor.throttle = 0 #Stops separating (1st half)

            while ((sys_flags.VERTICALITY == Verticality.NOT_UPRIGHT) or (sys_flags.MOVEMENT == Movement.MOVING)): #The second part of separation won't happen it the nosecone is not upright or moving
                continue

            motor.throttle = 1 #Will perform the second half of separation once it detects no movement or if it is upright
            time.sleep(HALF_SEPARATION_TIME) 
            motor.throttle = 0 #Stops separating (2nd half)

            # Release all retracted solenoids
            for solenoid in solenoids:
                solenoid.throttle = 0
            
            sys_flags.SEPARATED = Separated.SEPARATED

            ##### EXTEND CAMERA PHASE
            while((sys_flags.VERTICALITY == Verticality.NOT_UPRIGHT) or (sys_flags.MOVEMENT == Movement.NOT_MOVING)):
                continue

            camarm.extend()
            
            sys_flags.DEPLOYED = Deployed.DEPLOYED


def telemetryRoutine():
    # data we send back to base station
    telemetry.transmit("TEST")


def controlRoutine(currentState, currRAFCO_S, currRAFCO):
    if (sys_flags.STAGE_INFO == Stage.LANDED):
        RAFCOS_LIST = APRS.updateRAFCO() # READ ONLY list of ALL (including past) received APRS RAFCOS (rafco sequence)

        # Check if any unprocessed or is processing rafco in list (guaranteed to transition out of wait state)
        if (len(RAFCOS_LIST) > currRAFCO_S):
            newState = fsm.FSM(currentState, RAFCOS_LIST[currRAFCO_S], currRAFCO)
            
            # If FSM complete (i.e. returned to a wait state)
            currRAFCO += 1  # Increment to next RAFCO
            if (newState == fsm.State.WAIT):
                currRAFCO_S += 1    # Increment to next RAFCO_S when FSM has completed
                currRAFCO = 0
            
            return newState, currRAFCO_S, currRAFCO # Return FSM's new state
        
        return currentState, currRAFCO_S, currRAFCO # If no RAFCO, do not call FSM and return original state 
        


'''
NOTES:
Payload mission has 3 stages of execution
1. Awaiting launch
2. Awaiting landing 
3. Awaiting RAFCO   (FSM)

Transition Factors:
1->2
- Detects motion
- Altitude increases (detect apogee) + Lower pressure -- from the same sensor

2->3
- Detects no motion (need to determine amount of sensitivity to motion)
- Is upright
- Ground level altitude + Sea level pressure -- from the same sensor

'''

def test():
    currentState = fsm.State.WAIT
    currRAFCO_S = 0
    currRAFCO = 0

    while (True):
        currentState, currRAFCO_S = controlRoutine(currentState, currRAFCO_S, currRAFCO)

def main():
    """ INITIALIZATION PHASE """
    ### Generic global config
    # Set current flight stage to prelaunch
    sys_flags.STAGE_INFO = Stage.PRELAUNCH
    midair_oneshot_transition = False
    landed_oneshot_transition = False

    # Init FSM starting state
    state = fsm.State.WAIT
    currRAFCO = 0   # Index within RAFCOS_LIST for first unprocessed RAFCOS (rafco sequence)

    ### Component config
    motor, solenoids = motive_config.electromotives_config()
    bno, bmp = avionics_config.init_avionics()
    camera = imaging_config.init_avionics()
    # BMP or BNO hardware fault
    if (bno == None or bmp == None):
        sys_flags.WARN_AVIONICS = Warn_Avionics.WARNING
    # PiCamera hardware fault
    if (camera == None):
        sys_flags.WARNCAMERA = Warn_Camera.WARNING

    ### Delta timing frequencies
    # AVIONIC
    AVIONIC_FREQ = 100 # bno frequncy per second -- check documentations

    # TELEMETRY
    TELEMETRY_FREQ = 1

    # CONTROL
    CONTROL_FREQ = 2

    """ Main delta timing loop (HIGHEST ROUTINE PRIORITY FROM TOP) """

    time_last_sample = time.time()   # Reset delta timing
    while(True):
        # AVIONIC ROUTINE
        time_this_sample = time.time()
        if(time_this_sample - time_last_sample >= AVIONIC_FREQ):
            time_last_sample = time_this_sample
            avionicRoutine()

        # TELEMETRY ROUTINE
        time_this_sample = time.time()
        if(time_this_sample - time_last_sample >= TELEMETRY_FREQ):
            time_last_sample = time_this_sample
            telemetryRoutine()

        # CONTROL ROUTINE
        time_this_sample = time.time()
        if(time_this_sample - time_last_sample >= CONTROL_FREQ):
            time_last_sample = time_this_sample
            state, currRAFCO = controlRoutine(state, currRAFCO)
        

        # TRANSITION ONESHOTS
        if (sys_flags.STAGE_INFO == Stage.MIDAIR and midair_oneshot_transition == False):
            midair_oneshot_transition = True
            # do single transition to midair stuff here

        if (sys_flags.STAGE_INFO == Stage.LANDED and landed_oneshot_transition == False):
            landed_oneshot_transition = True
            deployRoutine(motor, solenoids) # Deploy imaging system
            aprs_subprocess = APRS.begin_APRS_recieve() # Begin listening for APRS commands


if __name__ == '__main__':
    # main() # real function
    test() # testing purposes