#run this bash command first
# rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin > data.txt

#HOW IT WORKS
#uses rtl_fm software to listen on freq 144.390(megahertz) at a sample rate of 22050 (universal standard) then pipe that information into software
#multimon-ng and decode it using the AFSK1200 standard then pipe that output to a text file

#PYTHON PORTION

#open text file in read mode
text_file = open("data.txt", "r")
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()

#make string into a list
transmission = data.split()

#show us the list
print(transmission)
