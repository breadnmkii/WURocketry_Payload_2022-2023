WAIT = 0
CALL = 1
READ = 2
EXEC = 3

def recieveRF(signal): #Lists out the signals and its components to it (called execute)
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
		currentState = CALL #Changes currentStte when call recieved

		if(data == teamRF(call)): #Checks to see if the call is ours
			currentState = EXEC 
			FSM(currentState) #Will make currentState to execute condition, follows FSM function (see line 15)
			currentState = WAIT #Back to wait condition once it's done, restarting the cycle

		else:
			currentState = WAIT #Goes back to wait condition if call is not ours


	
