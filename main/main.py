# FILE FOR MAIN PAYLOAD MISSION ROUTINE

## Imports
from Control import fsm
from Avionics import config as avionics_config
from Avionics import sensing
from Imaging import imaging
from Radio import APRS

## Globals
# SYS ARRAY: [isMoving, hitApogee, hasDeployed]
sys_flags = []


def update_imageCommands():
    with open("/Users/loganfarrow/Documents/data.txt") as file:
        imageCommands = []

        data = file.readlines()

        for line in data:
            cleanLine = line.strip("\n,;").split(" ")
            cleanLine = list(filter(None, cleanLine))
            
            imageCommands.append(cleanLine)
            
        return imageCommands
















# Payload mission functions (base on payload mission execution flowchart??)
def avionicRoutine(stage):
    stage_control(stage)
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

def stage_control(stage):
    # switch stages
    if (stage == 1 and sensing.detectMovement(acc_accumulator) and sensing.altitude_status(altitude_accumulator, pressure_accumulator) == 'up'):
        stage = 2
    if (stage == 2 and sensing.remain_still(acc_accumulator) and sensing.ground_level(altitude_accumulator, pressure_accumulator)):
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

def FSM(stage):
    rfRecieved = True
    while(stage == 3):
<<<<<<< HEAD
    
    
        currentState = fsm.State.WAIT #Initial waiting condition

        while True:
            call = "XD71" #Brief outline of the call that we will recieve from our call variable
            data = APRS.update_imageCommands() #Put in that call into this function
            currentState = fsm.State.CALL #Changes currentState when call recieved

            if(data == teamRF(call)): #Checks to see if the call is ours
                currentState = fsm.State.EXEC 
                FSM(currentState) #Will make currentState to execute condition, follows FSM function (see lines 15-20)
                currentState = fsm.State.WAIT #Back to wait condition once it's done, restarting the cycle

            else:
                currentState = fsm.State.WAIT #Goes back to wait condition if call is not ours
        
            fsm.FSM(currentState, fsm.sequence, fsm.sequenceBuffer)
   
=======
        fsm.FSM(fsm.State.WAIT, fsm.seque)
        '''
        if fsm.receiveRF():
            fsm.FSM(fsm.State.CALL, fsm.sequence, fsm.sqeuenceBuffer)
        else:
            fsm.FSM(fsm.State.WAIT, fsm.sequence, fsm.sqeuenceBuffer)
        '''
>>>>>>> df1586aa9ad493cef6dced5fa1d9fba4517c21b5

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