################################################
######## MAIN PAYLOAD MISSION ROUTINE ##########
################################################

### IMPORTS ###
# from Avionics import config as avionics_config
# from Imaging import config as imaging_config  # DEPRECATED

#from Motive import config as motive_config

# from Avionics import sensing
from Control import fsm
#from Motive import camarm
from Radio import APRS
from Radio import telemetry

import time
import datetime
from enums import *
import signal
import sys
import re



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
CALLSIGN = "KQ4CTL-6"               # Nasa's callsign

### PAYLOAD ROUTINE FUNCTION ###
# Sensing
def avionicRoutine():
    # initialize values
    has_launched = None # sensing.detectMovement(acc_accumulator) # true means launch detected, false means launch not detected
    is_still = None # sensing.remain_still(acc_accumulator) # true means still, false means not still
    is_upright = None
    heat = None
    bmp_values_status = None # sensing.altitude_status(altitude_accumulator, pressure_accumulator)
    ground_steady = None

    ### PRE-LAUNCH STANDBY ###
    if(sys_flags.STAGE_INFO == Stage.PRELAUNCH):
        has_launched = avionics_prelaunch()
    elif (sys_flags.STAGE_INFO == Stage.MIDAIR):
        # sample for movement (if launched)
        (heat, is_still, ground_steady, bmp_values_status) = avionics_midair()
    elif (sys_flags.STAGE_INFO == Stage.LANDED):
        # check for no movement (if landed)
        # check for upright (orientation sensor)
        (heat, is_still, is_upright) = avionics_landed()

    # update system flags -- specifics (related to avionics)
    #print("update sysflags")
    print(is_upright, heat, bmp_values_status, has_launched, is_still, ground_steady)
    update_system_flags(is_upright, heat, bmp_values_status, has_launched, is_still, ground_steady)

def avionics_prelaunch():
    acceleration_buffer = sensing.read_acceleration_buffer()
    has_launched = sensing.detectLaunch(acceleration_buffer)
    print('is it launched yet?', has_launched)
    # is_still = sensing.remain_still(acceleration_buffer)
    return (has_launched)

def avionics_midair():
    acceleration_buffer = sensing.read_acceleration_buffer()
    (temperature_buffer, pressure_buffer, altitude_buffer) = sensing.read_bmp()
    bmp_values_status = sensing.altitude_status(altitude_buffer, pressure_buffer)
    heat = sensing.check_heat(temperature_buffer)
    is_still = not(sensing.detectMovement(acceleration_buffer))
    print('is it still?', is_still)
    ground_steady = sensing.ground_level(altitude_buffer, pressure_buffer)
    return (heat, is_still, ground_steady, bmp_values_status)

def avionics_landed():
    euler_buffer = sensing.read_euler_buffer()
    acceleration_buffer = sensing.read_acceleration_buffer()
    (temperature_buffer, pressure_buffer, altitude_buffer) = sensing.read_bmp()
    heat = sensing.check_heat(temperature_buffer)
    is_still = sensing.remain_still(acceleration_buffer)
    is_upright = sensing.vertical(euler_buffer)
    return (heat, is_still, is_upright)

def update_system_flags(is_upright, heat, bmp_values_status, has_launched, is_still, ground_steady):
    if is_upright:
        sys_flags.VERTICALITY = int(is_upright == True) 
    if heat:
        sys_flags.WARN_HEAT = int(heat == True) 
    if bmp_values_status:
        if sys_flags.MOVEMENT == Movement.MOVING and bmp_values_status == 'up':
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.MOVING_UP
        elif sys_flags.MOVEMENT == Movement.MOVING and bmp_values_status == 'down':
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.MOVING_DOWN
        elif sys_flags.MOVEMENT == Movement.MOVING and bmp_values_status == 'moving':
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.MOVING
        else:
            sys_flags.FLIGHT_DIRECTION = Flight_Direction.INDETERMINENT

    if has_launched and is_still:
        if has_launched and not is_still:
            sys_flags.MOVEMENT = Movement.MOVING
        elif not has_launched and  is_still:
            sys_flags.MOVEMENT = Movement.NOT_MOVING
        else:
            sys_flags.MOVEMENT = Movement.CONFLICTING_DECISION
            print('NOTICE: sensor uncertain of movement ')

    # switch stages
    if (sys_flags.STAGE_INFO == Stage.PRELAUNCH and has_launched and (bmp_values_status == 'up' or bmp_values_status == 'moving')):
        sys_flags.STAGE_INFO = Stage.MIDAIR

    if (sys_flags.STAGE_INFO == Stage.MIDAIR and is_still and ground_steady):
        sys_flags.STAGE_INFO = Stage.LANDED

# Deployment
SEPARATION_TIME = 75   # Seconds
RETRACT_TIME = 50
#motor, solenoids = motive_config.electromotives_config()

### FAILSAFE ABORT ###
# SIGINT abort
def abort_motives(sig, frame):
    motor.throttle = 0
    solenoids.throttle = 0
    sys.exit(0)
signal.signal(signal.SIGINT, abort_motives)

def deployRoutine(motor, solenoids):
    if (sys_flags.STAGE_INFO == Stage.LANDED):
        if (sys_flags.DEPLOYED == Deployed.NOT_DEPLOYED):
            ##### REALIGN (New phase, need to "pull" nosecone back a bit to release retention)
            """ DEPRECATED - Racks not connected to nosecone """
            # motor.throttle = -1
            # time.sleep(0.5)
            # motor.throttle = 0
            
            ##### RETENTION RELEASE PHASE
            #The soleonid will not retract in if it detects movement
            print("Releasing solenoids...")
            while (sys_flags.MOVEMENT == Movement.MOVING): 
                print("wait stable...")
                continue

            # Retract all solenoids in retention
            solenoids.throttle = 1

            print("Released solenoids!")
            time.sleep(3)

            # Release all solenoids in retraction
            solenoids.throttle = 0
                
            ##### SEPARATION PHASE
            # Wait until stable to separate
            print("Separating bay...")
            while (sys_flags.MOVEMENT == Movement.MOVING):
                print("wait stable...")
                continue
            print(f"Separating for {SEPARATION_TIME}s")
            motor.throttle = 1 # Motorhat will separate forward once it's not moving
            time.sleep(SEPARATION_TIME) 
            motor.throttle = 0 # Stops separating
            
            print("Separated!")
            time.sleep(0.5)
            
            print(f"Retracting racks for {RETRACT_TIME}")
            motor.throttle = -1
            time.sleep(RETRACT_TIME)
            motor.throttle = 0

            print("Retracted!")
            time.sleep(0.5)
            
            sys_flags.SEPARATED = Separated.SEPARATED
            print("~ System separated ~")

            ##### EXTEND CAMERA PHASE
            print("Extending camarm...")
            # Wait until stable and upright to deploy camarm
            while((sys_flags.VERTICALITY == Verticality.NOT_UPRIGHT) or (sys_flags.MOVEMENT == Movement.NOT_MOVING)):
                print("wait stable upright...")
                continue
            print("Extending...")
            camarm.extend()

            
            print("Extended!")
            time.sleep(0.5)
            camarm.setzero()
            
            sys_flags.DEPLOYED = Deployed.DEPLOYED
            
            print("~ System deployed ~")

# Telemetry
def telemetryRoutine():
    current_time = datetime.datetime.now()
    sys_flags_pkt = sys_flags.get_bitmask_str()

    packet = f'{current_time} {sys_flags_pkt}'
    telemetry.transmitData(packet)

# APRS
def updateRAFCO():
    imageCommands = []
    current_command_list = [CALLSIGN]
    valid_commands = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8']

    with open(APRS_LOG_PATH, "r") as file:
        filelines = []
        for line in file:
            filelines.append(line)
        
        
        for i in range(0, len(filelines)):
            if CALLSIGN in filelines[i] and i+1 < len(filelines):
                
                line = filelines[i+1].replace(":"," ").strip()
                if line:
                    print('line?????')
                    # Split the line into words and remove the colon ':' if it exists
                    words = re.sub(r'[^\w\s]', ' ', line) #replace all special characters with a space
                    words = re.sub(r'[^A-H1-8\s]', ' ', words) #replace all things that are not A->H and 1->8 with a space
                    words = words.split(" ")

                    for word in words:
                        if word in valid_commands:
                            current_command_list.append(word)

                # Append current_command_list to imageCommands and reset it for the next line
                if current_command_list:
                    imageCommands.append(current_command_list)
                    current_command_list = [CALLSIGN]
                
    return imageCommands

# Control
def controlRoutine(currentState, currRAFCO_S_idx, currRAFCO_idx):
    if (sys_flags.STAGE_INFO == Stage.LANDED):
        RAFCOS_LIST = updateRAFCO() # READ ONLY list of ALL (including past) received APRS RAFCOS (rafco sequence)
        

        # Check if any unprocessed or is processing rafco in list (guaranteed to transition out of wait state)
        if (len(RAFCOS_LIST) > currRAFCO_S_idx):
            print(f"Current RAFCO Log: {RAFCOS_LIST}")

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
    currentState = fsm.State.WAIT
    currRAFCO_S_idx = 0
    currRAFCO_idx = 0   # Index within RAFCOS_LIST for first unprocessed RAFCOS (rafco sequence)

    ### Component config
    motor, solenoids = motive_config.electromotives_config()
    bno, bmp = avionics_config.init_avionics()
    # BMP or BNO hardware fault
    if (bno == None or bmp == None):
        sys_flags.WARN_AVIONICS = Warn_Avionics.WARNING

    ### Delta timing frequencies
    # AVIONIC
    AVIONIC_FREQ = 1/100 # bno frequncy -- check documentations
    avionic_last_time = 0

    # TELEMETRY
    TELEMETRY_FREQ = 1
    telemetry_last_time = 0

    # CONTROL
    CONTROL_FREQ = 1/2
    control_last_time = 0

    """ Main delta timing loop (HIGHEST ROUTINE PRIORITY FROM TOP) """

    while(True):
        # AVIONIC ROUTINE
        this_time = time.time()
        if(this_time - avionic_last_time >= AVIONIC_FREQ):
            avionic_last_time = this_time + AVIONIC_FREQ
            avionicRoutine()

        # TELEMETRY ROUTINE
        this_time= time.time()
        if(this_time - telemetry_last_time >= TELEMETRY_FREQ):
            telemetry_last_time = this_time + TELEMETRY_FREQ
            telemetryRoutine()

        # CONTROL ROUTINE
        this_time = time.time()
        if(this_time - control_last_time >= CONTROL_FREQ):
            control_last_time = this_time + CONTROL_FREQ
            fsmUpdate = controlRoutine(currentState, currRAFCO_S_idx, currRAFCO_idx)
            currentState = fsmUpdate[0]
            currRAFCO_S_idx = fsmUpdate[1]
            currRAFCO_idx = fsmUpdate[2]
        

        ### STAGE TRANSITION ONESHOT EXECUTIONS ###
        if (sys_flags.STAGE_INFO == Stage.MIDAIR and midair_oneshot_transition == False):
            print("Stage 2 Entered!")
            midair_oneshot_transition = True
            # do single transition to midair stuff here

        if (sys_flags.STAGE_INFO == Stage.LANDED and landed_oneshot_transition == False):
            print("Stage 3 Entered!")
            landed_oneshot_transition = True
            
            # deployRoutine(motor, solenoids) # Deploy imaging system
            aprs_subprocess = APRS.begin_APRS_recieve(APRS_LOG_PATH) # Begin listening for APRS commands

def test_main():
    # print("Reading APRS transmissions...")
    # while True:
    #     print(updateRAFCO())

    """ Telemetry avionics test """
    # sys_flags.STAGE_INFO = Stage.PRELAUNCH
    
    # while (True):
    #  avionicRoutine()
    #  telemetryRoutine()

    """ FSM TEST """
    currentState = fsm.State.WAIT
    currRAFCO_S_idx = 0
    currRAFCO_idx = 0

    sys_flags.STAGE_INFO = Stage.LANDED # Override to mission execution phase (to enable FSM routine)
    APRS.begin_APRS_recieve(APRS_LOG_PATH)   # Begin APRS receiving process at specified file (comment out if APRS_log exists in main directory)

    while (True):
        fsmUpdate = controlRoutine(currentState, currRAFCO_S_idx, currRAFCO_idx)
        currentState = fsmUpdate[0]
        currRAFCO_S_idx = fsmUpdate[1]
        currRAFCO_idx = fsmUpdate[2]


if __name__ == '__main__':
    test_main()



