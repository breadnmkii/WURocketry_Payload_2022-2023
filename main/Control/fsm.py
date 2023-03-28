## FSM Python Program
# Responsible for processing RAFCO buffer received by APRS program
# Input:	(likely) file reader (that is continuously updated by Logan's APRS
#			bash script)
#				OR
# 			formatted as list headed with team's CALLSIGN and a sequence of 
# 			2-char RAFCO character data. (made possible by Logan's Py wrapper)

# DEBUG NOTE: assume team CALLSIGN is XD71

import random
from enum import Enum
import time
import sys
#from Imaging import imaging
from Motive import camarm

CALLSIGN = "XD71" # NASA's callsign (FSM only responds to RAFCO sequences headed by this callsign)

# States enum
class State(Enum):
	WAIT = 0		# default state where program is awaiting new input
	CALL = 1		# state that reads input and checks if CALLSIGN is ours
	READ = 2		# state that reads a single RAFCO
	EXEC = 3		# state that executes AND WAITS for physical completion

## THIS IS THE MAIN FSM PROGRAM
# A function that changes state depending on state and input (Mealy machine)
# Inputs:
# - currRAFCO_S: list of RAFCO
# - idx: index into currRAFCO_S 
def FSM(state, currRAFCO_S, idx): 
	
	if state == State.WAIT:
		# if sequence is not empty
		if (len(currRAFCO_S) > 0):
			state = State.CALL
		else:
			state = State.WAIT

	elif state == State.CALL:
		# Look for NASA CALLSIGN in RAFCO sequence and change to exec if found
		print(f'~~ Verifying {currRAFCO_S}')
		if (CALLSIGN in currRAFCO_S):
			print("Valid RAFCO_S")
			state = State.EXEC
		else:
			print("Invalid RAFCO_S")
			state = State.WAIT

	elif state == State.EXEC:
		# Grab first RAFCO from currently executing sequence (Should always be at idx+1 position)
		idx += 1
		if (idx < len(currRAFCO_S)):
			RAFCO = currRAFCO_S[idx]

			# Execute RAFCO
			if (RAFCO == "A1"):
				#camarm.set_zero()
				#camarm.main()
				print("A1: servo 60 degrees right")
				camarm.right_60()
				
			elif (RAFCO == "B2"):
				#camarm.set_zero()
				#camarm.main()
				print("B2: servo 60 degrees left")
				camarm.left_60()
				
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
				print(f'Non-RAFCO ({RAFCO}): Did not execute')

		else:
			# Finished executing current RAFCO sequence, return to waiting
			state = State.WAIT

	else:
		# default case to wait
		state = State.WAIT

	return (state, idx)