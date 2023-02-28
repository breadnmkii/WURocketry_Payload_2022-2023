# FILE FOR MAIN PAYLOAD MISSION ROUTINE

## Imports
from Control import fsm
from Avionics import config as avionics_config
from Avionics import sensing
from Imaging import imaging
from Radio import APRS

## Globals
'''
SYS ARRAY: [isMoving, hitApogee, hasDeployed]
sys_flags index 0: stage information, index 1: movement_decision, index 2: altitude_status
at index 1: 0 means not moving, 1 means moving, 2 conflicting decisions
at index 2: 0 means moving up, 1 means moving down, 2 indeterminant 
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
    has_launched = sensing.detectMovement(acc_accumulator) # true means movement detected, false means movement not detected
    is_still = sensing.remain_still(acc_accumulator) # true means still, false means not still
    if has_launched and not is_still:
        sys_flags[1] = 1
    elif not has_launched and  is_still:
        sys_flags[1] = 0
    else:
        sys_flags[1] = 2
        print('ATTENTION: linear acceleration and quarternion info not enough to determine the presence/absence of movement ')
    
    bmp_values_status = sensing.altitude_status(altitude_accumulator, pressure_accumulator)
    if sys_flags[1] == 1 and bmp_values_status == 'up':
        sys_flags[2] = 0     
    elif sys_flags[1] == 1 and bmp_values_status == 'down':
        sys_flags[2] = 1
    else:
        sys_flags[2] = 2

    if(stage == 1):
        sys_flags[0] = 1
        pass
        # sample for movement (if launched)
    elif (stage == 2):
        pass
        # check for no movement (if landed)
    elif (stage == 3):
        pass
        # check for upright (orientation sensor)

    # Update sys flags (related to avionics)
    # switch stages
    if (stage == 1 and sensing.detectMovement(acc_accumulator) and sensing.altitude_status(altitude_accumulator, pressure_accumulator) == 'up'):
        stage = 2
    if (stage == 2 and sensing.remain_still(acc_accumulator) and sensing.ground_level(altitude_accumulator, pressure_accumulator)):
        stage = 3

    if 

def controlRoutine():
    pass

def imageRoutine(stage):
    if (stage != 3):
        pass
    # cam stuff


def telemetryRoutine(stage):
    # data we send back to base station
    telemtery.transmit("data")

def FSM(stage):
    rfRecieved = True
    while(stage == 3):
    
    
        currentState = fsm.State.WAIT #Initial waiting condition

        while True:
            call = "XD71" #Brief outline of the call that we will recieve from our call variable
            data = APRS.update_imageCommands() #Put in that call into this function
            currentState = fsm.State.CALL #Changes currentState when call recieved

            if(data == call): #Checks to see if the call is ours
                currentState = fsm.State.EXEC 
                FSM(currentState, data) #Will make currentState to execute condition, follows FSM function (see lines 15-20)
                currentState = fsm.State.WAIT #Back to wait condition once it's done, restarting the cycle

            else:
                currentState = fsm.State.WAIT #Goes back to wait condition if call is not ours
        
            fsm.FSM(currentState, fsm.sequence, fsm.sequenceBuffer)
   

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
    # Component config and init
    (bno, bmp) = avionics_config.init_avionics()
    
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

    stage = 1
    ### Main delta timing loop
    aprs_begin = False
    while(True):
        avionicRoutine(stage)

        imageRoutine(stage)
        
        if (sys_flags[0]):
            stage = 2


        if (hasLanded):
            stage = 3

        if(stage == 3 and aprs_begin == False):
            aprs_subprocess = APRS.begin_APRS_recieve()
            aprs_begin = True

    # Delta timing loop