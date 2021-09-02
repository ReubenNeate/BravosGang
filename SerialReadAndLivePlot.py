#Written by Reuben Neate for EPR410

import matplotlib.pyplot as plt #import matplotlib library
import numpy as np #import numpy library
import serial #import Serial Library

##############################################################################
#Start by setting up the serial connection
#Choose the Com port and the Baud rate
#The connection we will call SerialPort
SerialPort = serial.Serial('COM7', 115200, bytesize=serial.EIGHTBITS, \
  parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

##############################################################################
#Declare the variables that need to be declared
N = 64  #We will aim for an N=64 to start with
SR = 80 #The system sampling rate
counter = 0 #Create a counter for the amount of data points received
FFT_data = np.zeros(N//2)
x = np.linspace(1, SR//2, N//2)  #Create x as the x axis variable

##############################################################################
#Create the plot that we will use
plt.ion()  #We are creating an intereactive graph
fig = plt.figure()  #Declare the figure
ax = fig.add_subplot(111)  #Add our plot
 #Create the first plot before any data is received
line1, = ax.plot(x, FFT_data, 'b-', label = 'Received FFT data')
#leg = ax.legend()  #Setup a legend
plt.ylim(-20, 100) # set the ylimit
plt.ylabel('Amplitude (dB)') #Label the axes
plt.xlabel('Frequency (Hz)')
plt.show
  

##############################################################################
#Update the plot witht the latest data
#Create a function that can be called from the main loop
def Updateplot(DataSet):
    global x, fig, line1, ax #The global variables that will be needed here
    line1.set_ydata(DataSet) #Update line1's data
    #Need the smallest pause for the data to update you can try without it 
    # to speed up the system but it often creates issues
    plt.pause(0.000002)                        
    ax.relim()  #I'm not sure what this does but it is needed
    fig.canvas.draw()  #And then this updates the figure

##############################################################################
#Run the main program flow here

try: #Create an infinte loop of checking for serial data
    #To end the infinite loop press 'ctrl' + 'C'. Sometimes you may need to
    #do it a few times, I don't know why
    while True:
        #First we need to receive the serial data
        counter = 0 #Start with the counter at 0
        while (counter < N//2): #Need to receive N/2 data points
            #wait untill the next data point is received
            while(SerialPort.inWaiting() == 0):
                pass
            #read in the latest datapoint that was just received
            #.decode() turns he data into a number because the arduino println
            #command I used. For the final version this may need to be changed
            FFT_data[counter] = SerialPort.readline().decode() 
            counter +=1 #increase the counter            
        #Now we update the data with the previously defined function
        Updateplot(FFT_data)
    
except KeyboardInterrupt: #When ctrl C is pressed it should close the serial 
    SerialPort.close() #connection.
    
#If it when you run the program it says that a serial connection is not 
#available try copying and pasting "SerialPort.close()" into the Python console
#and the pressing enter. Then try run again. Otherwise check nothing else is 
#using that connection


##############################################################################
