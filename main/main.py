# FILE FOR MAIN PAYLOAD MISSION ROUTINE

## Imports
from Control import fsm
from Avionics import config as avionics_config
from Avionics import sensing
from Imaging import imaging
from Imaging import config as camera_config
from Radio import APRS
import time

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


def update_imageCommands():
    with open("data") as file:
        imageCommands = []

        data = file.readlines()

        for line in data:
            cleanLine = line.strip("\n,;").split(" ")
            cleanLine = list(filter(None, cleanLine))
            
            imageCommands.append(cleanLine)
            
        return imageCommands
















# Payload mission functions (base on payload mission execution flowchart??)
def avionicRoutine(stage):
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
    if(stage == 0):
        (has_launched, is_still) = avionics_prelaunch()
    elif (stage == 1):
        # sample for movement (if launched)
        (has_launched, heat, is_still, ground_steady, bmp_values_status) = avionics_midair()
    elif (stage == 2):
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
        sys_flags[3] = int(is_upright == True) 
    if heat:
        sys_flags[6]  = int(heat == True) 
    if bmp_values_status:
        if sys_flags[1] == 1 and bmp_values_status == 'up':
            sys_flags[2] = 0     
        elif sys_flags[1] == 1 and bmp_values_status == 'down':
            sys_flags[2] = 1
        else:
            sys_flags[2] = 2

    if has_launched and is_still:
        if has_launched and not is_still:
            sys_flags[1] = 1
        elif not has_launched and  is_still:
            sys_flags[1] = 0
        else:
            sys_flags[1] = 2
            print('ATTENTION: linear acceleration and quarternion info not enough to determine the presence/absence of movement ')
    # Update sys flags
    # switch stages
    if (stage == 1 and has_launched and bmp_values_status == 'up'):
        stage = 2
    if (stage == 2 and is_still and ground_steady):
        stage = 3

def controlRoutine():
    pass

def imageRoutine(stage):
    if (stage != 3):
        pass
    # cam stuff


def telemetryRoutine(stage):
    # data we send back to base station
    telemtery.transmit("data")

def fsmRoutine(stage, currentState):
    while(stage == 3):
        
        call = "XD71" #Brief outline of the call that we will recieve from our call variable
        data = APRS.update_imageCommands() #Put in that call into this function
        currentState = fsm.State.CALL #Changes currentState when call recieved

        rafCall = data[0]


        if(data == call): #Checks to see if the call is ours
            currentState = fsm.State.EXEC 
            fsm.FSM(currentState, rafCall) #Will make currentState to execute condition, follows FSM function (see lines 15-20)
            currentState = fsm.State.WAIT #Back to wait condition once it's done, restarting the cycle

        else:
            currentState = fsm.State.WAIT #Goes back to wait condition if call is not ours
        
   

    pass


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
    # Init FSM starting state
    currentState = fsm.State.WAIT
    # Component config and init
    (bno, bmp) = avionics_config.init_avionics()
    camera = camera_config.init_avionics()
    # BMP or BNO hardware fualt
    if bno == None or bmp == None:
        sys_flags[8] = 1
    # PiCamera hardware fault
    if camera == None:
        sys_flags[7] = 1
    # right now, only BNO frequency used, ask whether two machines sampled at different rate
    BNO_FREQUENCY = 100 # bno frequncy per second -- check documentations
    BMP_FREQUENCY = 100 # bmp frequncy per second    
    '''
    ### Stage 1
    while(hasNotLaunched):
        routines()
        
        if(hasLaunched):
            break

    ### Stage 2 -- motion detected
    while(sensing.detectMovement(acc_accumulator)):
        rotunines()

        if(landed):
            break

    ### Stage 3
    while(sensing.remain_still(acc_accumulator)):
        pass
    '''

    """ ALTERNATIVE """

    #stage = 1
    sys_flags[0] = 0
    ### Main delta timing loop
    aprs_begin = False

    time_last_sample = time.time()   # Reset delta timing
    while(True):
        time_this_sample = time.time()
        if(time_this_sample - time_last_sample >= BNO_FREQUENCY):
            time_last_sample = time_this_sample
            avionicRoutine(sys_flags[0])
        time_this_sample = time.time()
        imageRoutine(sys_flags[0])
        
        if (sys_flags[0]):
            stage = 2


        if (hasLanded):
            stage = 3

        if(stage == 3 and aprs_begin == False):
            aprs_subprocess = APRS.begin_APRS_recieve()
            aprs_begin = True
            currentState = fsmRoutine(stage, currentState)

    # Delta timing loop