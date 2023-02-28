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
from Imaging import imaging

# sys.path.append('../')
# from Imaging import filter_image
# from Imaging import take_picture

CALLSIGN = "XD71"

# States enum
class State(Enum):
	WAIT = 0		# default state where program is awaiting new input
	CALL = 1		# state that reads input and checks if CALLSIGN is ours
	READ = 2		# state that reads a single RAFCO
	EXEC = 3		# state that executes AND WAITS for physical completion

## THIS IS THE MAIN FSM PROGRAM
# A function that changes state depending on state and input (Mealy machine)
# Inputs:
# - sequenceBuffer: queue of received APRS signals, managed externally from FSM
# - sequence: a temp list for current sequence being processed
def FSM(state, sequence): 
	
	if state == State.WAIT:
		# if sequence is a command
		if (len(sequence) > 0):
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
				imaging.take_picture()
				
			elif (RAFCO == "D4"):
				print("D4: image color to grayscale")
				imaging.to_grayscale()
				
			elif (RAFCO == "E5"):
				# filter_image.greyscale2rgb()
				print("E5: image grayscale to color")
				imaging.to_color_mode()
				
			elif (RAFCO == "F6"):
				# filter_image.rotate()
				print("F6: image rotate")
				imaging.rotate()
				
			elif (RAFCO == "G7"):
				# filter_image.projective_transform()
				print("G7: special effects filter")
				imaging.rgb2bgr()
				
			elif (RAFCO == "H8"):
				print("H8: remove all filters")
				imaging.remove_filter()
			
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