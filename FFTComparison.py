#Written by Reuben Neat for EPR410

import matplotlib.pyplot as plt
import numpy as np
import time  #We want to compare efficiency of the program
import math as m

##############################################################################
#First we want to define our input siugnal

N = 256  #The number of samples
SR = 90  #The sampling rate used in Hz

t = np.linspace(0, 1, N) #time array
dx = t[1] - t[0] #Get the step size
f = np.linspace(0, 1/(2*dx), N//2) #frequency array

a = 256 #expected input amplitude from the ADC
freq = 15  #frequency of the signal
Y = a * np.sin(2*np.pi*freq*t)  #Define the input signal
#print(Y)

#Plot the input signal
plt.figure()
plt.plot(t,Y)

##############################################################################

##############################################################################
#For reference we will use the numpy FFT function to compare results and to 
#compare efficiency by comparing processing time

start = time.perf_counter()  #Get the starting time of the FFT algorithm


##############Start Numpy FFT function here
Y_np_FFT = np.fft.fft(Y) #Get the library fourier transform

Y_np_FFT = Y_np_FFT/N #Scale the vertical by N
##############End Numpy FFT function here

end = time.perf_counter()  #Get the finish time of the FFT algorithm
TimeDifference = end - start #get the time difference

#Print the time difference
print("The numpy fft library took", TimeDifference, "s to execute.")


plt.figure()
plt.plot(f, abs(Y_np_FFT[0:N//2]))


##############################################################################

##############################################################################
#Now try your own FFT function

#Because the twiddle factors won't be made each time but on startup they won't
# be include in the time sequence
#Create a Twiddle factor database
#Now we make a database  of the twiddle factors
twiddle = np.zeros(N,dtype=np.complex) #Create an empty complex array
for i in range(0,N):
  twiddle[i] =  np.exp(-((1j*2*np.pi*i)/N)) #Twiddle factor formula
  #twiddle[i] = np.cos((i*2*np.pi)/N)  + (1j*np.sin((i*2*np.pi)/N))

start = time.perf_counter()  #Get the starting time of the FFT algorithm

###########Start custom FFT function here

def OddEven (arr):  #Divide an array by it's indexes. Odd and even
    L = len(arr)  #length of the array
    z = np.zeros(L)  #empty array
    for i in range (0, int(len(arr)/2)): #Only need to loop through half the 
      z[i] = arr[2*i]  #length. Will place every even sample at the sfirst 
      z[L-i-1] = arr[L-(2*i)-1] #half and every odd sample at the second half
    return z     

YT = list(Y) #start by making a temp or a working array

for i  in range(0,int(m.log2(N))-1): #loop for each subdivision
  p = 2**i #a division factor
  for j in range(0,N,int(N/p)): #divide the subdivisions up
    YT[j:int(j+(N/p))] = OddEven(Y[j:int(j+(N/p))])
  Y = list(YT) #Make sure to update the signal as you go



#Finally we run the actual fft algorithm
YS = list(Y)
YT = np.zeros(N,dtype=np.complex) #Will be our Transformed data

#First we need to loop for each layer of the butterfly diagram
for i in range(0,int(m.log2(N))):
  s = -2**i #the skipping factor
  #Now we loop for each bin in the FFT
  for j in range(0,N): 
    if (j%(2**i) ==0): #Make the  skipping factor + or -
      s = s * -1    
    #Now we need to get the correct twiddle factors
    if s > 0: #If we retreiving from bellow
      twdA = 1
      twdB = twiddle[int((j*(N/(2**(i+1))))%N)]
    else:  #else retreive from above
      twdA = twiddle[int((j*(N/(2**(i+1))))%N)]
      twdB =  1
    
    #Now we just weight and add the two points together
    YT[j] = (twdA*YS[j]) + (twdB * YS[j+s]) 

    
  #print(" ")
  YS = list(YT)  


###########End custom FFT function here

end = time.perf_counter()  #Get the finish time of the FFT algorithm
TimeDifference = end - start #get the time difference

#Print the time difference
print("Your fft library took", TimeDifference, "s to execute.")

plt.figure()
plt.plot(f, YS[0:N//2])


##############################################################################
