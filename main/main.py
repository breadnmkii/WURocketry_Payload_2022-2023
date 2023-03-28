################################################
######## MAIN PAYLOAD MISSION ROUTINE ##########
################################################

### IMPORTS ###
# from Avionics import config as avionics_config
# from Imaging import config as imaging_config
# from Motive import config as motive_config

#from Avionics import sensing
#from Control import fsm
#from Motive import camarm
#from Radio import APRS
from Radio import telemetry

import time
import datetime
from enums import *



### GLOBALS ###

# System flags -- refer to enums.py
'''
at index 0: 0 means prelaunch standby stage, 1 means payload midair, 2 means payload landed
at index 1: 0 means not moving, 1 means moving, 2 conflicting decisions
at index 2: 0 means moving up, 1 means moving down, 2 indeterminant 
at index 3: 0 means not upright, 1 means vertical position for camera
at index 6: 1 means BMP senses averaged temperature above 83 Celcius
at index 7: 1 means PiCamera initialization fails -- hardware fault
at index 8: 1 means BNO or BMP initialization fails -- hardware fault

'''
sys_flags = System_Flags(Stage.PRELAUNCH, Movement.NOT_MOVING, Flight_Direction.INDETERMINENT, Verticality.NOT_UPRIGHT, Separated.NOT_SEPARATED, Deployed.NOT_DEPLOYED, Warn_Heat.NOMINAL, Warn_Camera.NOMINAL, Warn_Avionics.NOMINAL, Warn_Motive.NOMINAL)


APRS_LOG_PATH = "./APRS_log.log"    # APRS Log File Path

### PAYLOAD ROUTINE FUNCTION ###
# Sensing
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

# Deployment
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

# Telemetry
def telemetryRoutine():
    # basic data we send back to base station
    current_time = datetime.datetime.now()
    sys_flags_str = ' | '.join(sys_flags.get_str())

    packet = f'{current_time}: {sys_flags_str}'
    print(packet)
    telemetry.transmitData(packet)

# APRS
def updateRAFCO():
    imageCommands = []
    with open(APRS_LOG_PATH) as file:
        data = file.readlines()
        for line in data:
            cleanLine = line.strip().replace(",", "").split(" ")
            cleanLine = list(filter(None, cleanLine))
            imageCommands.append(cleanLine)
        file.close()
    return imageCommands

# Control
def controlRoutine(currentState, currRAFCO_S_idx, currRAFCO_idx):
    if (sys_flags.STAGE_INFO == Stage.LANDED):
        RAFCOS_LIST = updateRAFCO() # READ ONLY list of ALL (including past) received APRS RAFCOS (rafco sequence)

        # Check if any unprocessed or is processing rafco in list (guaranteed to transition out of wait state)
        if (len(RAFCOS_LIST) > currRAFCO_S_idx):
            fsmUpdate = fsm.FSM(currentState, RAFCOS_LIST[currRAFCO_S_idx], currRAFCO_idx)

            # Update fsm inputs
            currentState = fsmUpdate[0]
            currRAFCO_idx = fsmUpdate[1]

            print(currentState)

            # If FSM complete (i.e. returned to a wait state)
            if (currentState == fsm.State.WAIT):
                print(f'Processed RAFCO_S: {RAFCOS_LIST[currRAFCO_S_idx]}\n')
                currRAFCO_S_idx += 1    # Increment to next RAFCO_S when FSM has completed
                currRAFCO_idx = 0       # Seek back to beginning of RAFCO_S
                
            return (currentState, currRAFCO_S_idx, currRAFCO_idx) # Return FSM's new state inputs
        
    return (currentState, currRAFCO_S_idx, currRAFCO_idx) # If not execution stage or no RAFCO, do not call FSM and return original state
        

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

def test_main():
    currentState = fsm.State.WAIT
    currRAFCO_S_idx = 0
    currRAFCO_idx = 0

    sys_flags.STAGE_INFO = Stage.LANDED # Override to mission execution phase (to enable FSM routine)
    # APRS.begin_APRS_recieve(APRS_LOG_PATH)   # Begin APRS receiving process at specified file (comment out if APRS_log exists in main directory)

    while (True):
        '''
        fsmUpdate = controlRoutine(currentState, currRAFCO_S_idx, currRAFCO_idx)
        currentState = fsmUpdate[0]
        currRAFCO_S_idx = fsmUpdate[1]
        currRAFCO_idx = fsmUpdate[2]
        avionicRoutine()
        '''
        telemetryRoutine()


if __name__ == '__main__':
    test_main()
