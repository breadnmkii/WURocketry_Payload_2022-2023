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
		["WU22RC", "A1", "G7", "D4", "F6"],
		''' TODO: add extra test cases here (sequences that are not just our
					callsign) 
		'''
	]
	
	#run rtl_recieve.sh first

	#open text file in read mode
	text_file = open("transmission.txt", "r")

	#read whole file to a string
	transmission = text_file.read().split()
	
	#close file
	text_file.close()

	# return transmission

	return randomInputs[random.randint(0, len(randomInputs))]


## THIS IS THE MAIN FSM PROGRAM
# A function that changes state depending on only state (Moore machine)
# Reads each of the signal's components for that given signal and executes it
def FSM(state): 
	nextState	# the next state to be transitioned to
	
	# This is essentially a switch statement, but not available < Python 3.10
	if state == State.WAIT:
		if (receiveRF()):
			# if signal received (i.e. not empty list)
			nextState = State.CALL
		else:
			# else, keep on waiting
			nextState = State.WAIT

	elif state == State.CALL:
		if ( ''' TODO: what should this condition be? '''):
			nextState = State.READ
		else:
			nextState = State.WAIT

	elif state == State.READ:
		if ( ''' TODO: what should this condition be? ''' ):
			nextState = State.EXEC
		else:
			nextState = State.WAIT

	elif state == State.EXEC:

		''' TODO: fill this out so that you simulate a RAFCO and then 
					remove it from the list 
		'''

		nextState = State.READ

	else:
		# default cause to wait
		nextState = State.WAIT


def main():
	currentState = State.WAIT	#Initial waiting condition
	teamSign = "WU22RC"		# Assume this is our callsign
	
	# Main loop that continuously runs FSM
	while True:
		currentState = FSM(currentState)



	
