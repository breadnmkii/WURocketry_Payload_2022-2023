#open text file in read mode
from hmac import trans_36


text_file = open("data.txt", "r")
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()

#make string into a list
transmission = data.split()

#show us the list
print(transmission)
