## FSM Python Program
# Responsible for processing RAFCO buffer received by APRS program
# Input:	(likely) file reader (that is continuously updated by Logan's APRS
#			bash script)
#				OR
# 			formatted as list headed with team's callsign and a sequence of 
# 			2-char RAFCO character data. (made possible by Logan's Py wrapper)

# DEBUG NOTE: assume team callsign is WU22RC

import random
from enum import Enum

signalBuffer = [] #Queue to hold all other signals
callsign = "NASA22"

# States enum
class State(Enum):
	WAIT = 0		# default state where program is awaiting new input
	CALL = 1		# state that reads input and checks if callsign is ours
	READ = 2		# state that reads a single RAFCO
	EXEC = 3		# state that executes AND WAITS for physical completion


# This provides randomly selected RAFCO sequence signals (i.e. your test cases)
def receiveRF():
	randomInputs = [
		[],	# empty input
		["NASA22", "A1", "G7", "D4", "F6"],
		["TRASH", "NASA22", "A1", "F6", "D4"]
	]
	return randomInputs[random.randint(0, len(randomInputs))]


## THIS IS THE MAIN FSM PROGRAM
# A function that changes state depending on only state (Moore machine)
# Reads each of the signal's components for that given signal and executes it
def FSM(state): 
	nextState = 0	# the next state to be transitioned to
	# This is essentially a switch statement, but not available < Python 3.10
	if state == State.WAIT:
		input = receiveRF()
		if (input):
			# if signal received (i.e. not empty list)
			signalBuffer.append(input)
			nextState = State.CALL
		else:
			# else, keep on waiting
			nextState = State.WAIT

	elif state == State.CALL:
		for pkt in signalBuffer[0]:
			if (pkt == callsign):
				nextState = State.EXEC

		nextState = State.WAIT

	elif state == State.EXEC:
		for RAFCO in signalBuffer[0]:
			if (RAFCO == "A1"):
				print("exec1")
				#execA1()
			elif (RAFCO == "B2"):
				print("exec2")
				#execB2()
			elif (RAFCO == "C3"):
				print("exec3")
				#execC3()
			elif (RAFCO == "D4"):
				print("exec4")
				#execD4()
			elif (RAFCO == "E5"):
				print("exec5")
				#execE5()
			elif (RAFCO == "F6"):
				print("exec6")
				#execF6()
			elif (RAFCO == "G7"):
				print("exec7")
				#execG7()
			elif (RAFCO == "H8"):
				print("exec8")
				#execH8()
		
		signalBuffer.remove(0)
		nextState = State.WAIT

	else:
		# default cause to wait
		nextState = State.WAIT


def main():
	currentState = State.WAIT	#Initial waiting condition

	# Main loop that continuously runs FSM
	while True:
		currentState = FSM(currentState)
		
if __name__ == '__main__':
        main()

'''
WAIT = 0
CALL = 1
READ = 2
EXEC = 3

def recieveRF(signal): #Lists out the signals and its components to it (called executive)
	if(signal == "XD71"):
		executive = ["A1", "G7", "B2"]

	elif (signal == "XX4XXX"):
		executive = ["C3", "A1", "D4", "C3", "F6", "C3",...]

	return signal

def FSM(state): #Reads each of the signal's components for that given signal and executes it
	if(state == EXEC):
		for i in executive:
			return i
	
	return state

def main():
	currentState = WAIT #Initial waiting condition

	while True:
		call = "XD71" #Brief outline of the call that we will recieve from our call variable
		data = recieveRF(call) #Put in that call into this function
		currentState = CALL #Changes currentState when call recieved

		if(data == teamRF(call)): #Checks to see if the call is ours
			currentState = EXEC 
			FSM(currentState) #Will make currentState to execute condition, follows FSM function (see lines 15-20)
			currentState = WAIT #Back to wait condition once it's done, restarting the cycle

		else:
			currentState = WAIT #Goes back to wait condition if call is not ours
'''

	
