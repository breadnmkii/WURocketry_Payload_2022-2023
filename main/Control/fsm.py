## FSM Python Program
# Responsible for processing RAFCO buffer received by APRS program
# Input:	(likely) file reader (that is continuously updated by Logan's APRS
#			bash script)
#				OR
# 			formatted as list headed with team's CALLSIGN and a sequence of 
# 			2-char RAFCO character data. (made possible by Logan's Py wrapper)

# DEBUG NOTE: assume team CALLSIGN is WU22RC

import random
from enum import Enum
import time
import sys

sys.path.insert(1, '/home/pi/WURocketry_Payload_2022-2023/main/Imaging')
import imaging

# sys.path.append('../')
# from Imaging import filter_image
# from Imaging import take_picture

CALLSIGN = "NASA22"

# States enum
class State(Enum):
	WAIT = 0		# default state where program is awaiting new input
	CALL = 1		# state that reads input and checks if CALLSIGN is ours
	READ = 2		# state that reads a single RAFCO
	EXEC = 3		# state that executes AND WAITS for physical completion


# This provides randomly selected RAFCO sequence signals (i.e. your test cases)
def receiveRF():
	testcases = [
		[],	# empty input
		["NASA22", "CORRUPTED", "CORRUPTED"],
		["NASA22", "A1", "G7", "D4", "F6"],
		["CORRUPTED", "NASA22", "A1", "F6", "D4"],
		["NASA22", "B2", "CORRUPTED", "H8"],
		["NASA22", "A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8"]
	]
	return testcases[random.randint(0,len(testcases)-1)]


## THIS IS THE MAIN FSM PROGRAM
# A function that changes state depending on state and input (Mealy machine)
# Inputs:
# - sequenceBuffer: queue of received APRS signals, managed externally from FSM
# - sequence: a temp list for current sequence being processed
def FSM(state, sequence, sequenceBuffer): 
	
	if state == State.WAIT:
		# if sequenceBuffer has awaiting signals
		if (len(sequenceBuffer) > 0):
			sequence = sequenceBuffer.pop(0)
			state = State.CALL
		else:
			state = State.WAIT

	elif state == State.CALL:
		# Look for NASA CALLSIGN in RAFCO sequence and change to exec if found
		state = State.WAIT
		while (len(sequence) > 0):
			RAFCO = sequence.pop(0)		# Remove callsign or any corrupt RAFCO from sequence (optimization)
			if (RAFCO == CALLSIGN):
				state = State.EXEC
				break
			
	elif state == State.EXEC:
		# Grab first RAFCO from currently executing sequence
		if (len(sequence) > 0):
			RAFCO = sequence.pop(0)

			# Execute RAFCO
			# st = time.time()
			if (RAFCO == "A1"):
				print("A1: servo 60 degrees right")
				
			elif (RAFCO == "B2"):
				print("B2: servo 60 degrees left")
				
			elif (RAFCO == "C3"):
				# take_picture.camera_time()
				print("C3: take picture")
				
			elif (RAFCO == "D4"):
				print("D4: image color to grayscale")
				
			elif (RAFCO == "E5"):
				# filter_image.greyscale2rgb()
				print("E5: image grayscale to color")
				
			elif (RAFCO == "F6"):
				# filter_image.rotate()
				print("F6: image rotate")
				
			elif (RAFCO == "G7"):
				# filter_image.projective_transform()
				print("G7: special effects filter")
				
			elif (RAFCO == "H8"):
				print("H8: remove all filters")
			
			else:
				print("Corrupted RAFCO: Could not execute")
				
			# et = time.time_ns()
			# elasped = time.time() - st #Prints the time between th
			# print(f'Elapsed time (RAFCO): {elasped}')
			# print(f'Start time (RAFCO): {st}')
			# print(f'End time (RAFCO): {et}')

			# Save FSM cycle for checking empty sequence (optimization)
			if (len(sequence) <= 0):
				state = State.WAIT

		else:
			# Finished executing current RAFCO sequence, return to waiting
			state = State.WAIT

	else:
		# default case to wait
		state = State.WAIT

	return (state, sequence)


def main():
	print("MAIN HERE")
	deltaTime = 0
	
	while(deltaTime < 10):
		start = time.time_ns()
		imaging.rotate()
		end = time.time_ns()
		elasped = end - start
		print(f'Elasped time: {elasped}')
		deltaTime += 1

	'''
		imaging.greyscale2rgb()
		imaging.remove_filter()
		imaging.rgb2bgr()
		imaging.take_picture()
		end6 = time.time_ns()
		elasped = end - start
		print(elasped)
	'''

	'''
	sequenceBuffer = [] 		# Queue to hold all other signals
	currentState = State.WAIT	# Initial start state
	currentSequence = []		# Initial start sequence
	
	# Fill sequence buffer with 'n' random signals (max 9n RAFCO)
	# Note: In practice, this will be asynchronously updated with the APRS module 
	#       (runs with different frequency compared to FSM)
	n = 5

	print("= TESTCASE SEQUENCES =")
	for _ in range(n):
		tempseq = receiveRF()
		sequenceBuffer.append(tempseq)
		print(tempseq)

	# Run FSM for a maximum of 9n iterations
	print("= RUNNING FSM =")
	for _ in range(9*n):
		print("FSM State:", currentState)
		currentState, currentSequence = FSM(currentState, currentSequence, sequenceBuffer)
	'''	

if __name__ == '__main__':
	
	main()
	print("RAN MAIN")






'''
WAIT = 0
CALL = 1
READ = 2
EXEC = 3

def recieveRF(sequence): #Lists out the signals and its components to it (called executive)
	if(sequence == "XD71"):
		executive = ["A1", "G7", "B2"]

	elif (sequence == "XX4XXX"):
		executive = ["C3", "A1", "D4", "C3", "F6", "C3",...]

	return sequence

def FSM(state): #Reads each of the sequence's components for that given sequence and executes it
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