# FILE FOR MAIN PAYLOAD MISSION ROUTINE

## Imports
from Control import fsm

## Globals
# SYS ARRAY: [isMoving, hitApogee, hasDeployed]
sys_flags = []

# Payload mission functions (base on payload mission execution flowchart??)
def avionicRoutine(stage):
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
        if fsm.receiveRF():
            fsm.FSM(State.CALL, )

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
    bno055 = 1
    init = 2
    
    ### Stage 1
    while(hasNotLaunched):
        routines()
        
        if(hasLaunched):
            break

    ### Stage 2
    while(hasNotLanded):
        rotunines()

        if(landed):
            break

    ### Stage 3


    """ ALTERNATIVE """

    stage = 1
    ### Main delta timing loop
    while(True):
        avionicRoutine(stage)

        imageRoutine(stage)
        
        if (sys_flags[0]):
            stage = 2


        if (hasLanded):
            stage = 3



    # Delta timing loop