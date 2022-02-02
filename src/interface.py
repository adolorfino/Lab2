'''
    @file       task_user.py
    @brief      This file is responsible for the user interface of the motor commands.
    @details    Depending on the input of the user the task_user.py will zero the
                motor encoder, print the motor encoder position, print the motor
                encoder delta, collect data for 30 seconds and print as a list,
                and enter duty cycles. This can be done with either Motor 1 or 
                Motor 2 as specified by capital/lowercase letters.

    @author: Eddy Rodriguez
    @author: Chloe Chou
    @date: November 1, 2021
'''
from matplotlib import pyplot 
import serial

ser_port = serial.Serial("COM8", 115200)

x_axis = []
y_axis = []

S0_INIT = 0
S1_WAIT_FOR_CHAR = 1
S2_APPEND = 2
S3_PLOT = 3

state = S0_INIT
while True:
    if state == S0_INIT:
        print("__________________________________________________________________________________________")
        print("|Welcome, here are a list of commands for this device.                                    |")
        print("|_________________________________________________________________________________________|")
        state = S1_WAIT_FOR_CHAR
        
    elif state == S1_WAIT_FOR_CHAR:
        char_in = input("enter:")
        if True:
            try:
                print("test")
                if ser_port.in_waiting>0:
                    print("hi")
                    line = ser_port.readline()
                    row = line.split (b',')
                    print(line)
                    
                    print(row)
                    x = float(row[0])
                    y = float(row[1])
                    
                    x_axis.append(x)
                    y_axis.append(y)
                    
                    if line == b'end\n':
                        print("DONE")
                        state = 3
                    print("changing")
            except ValueError:
                pass
            except IndexError:
                pass
    elif state == S2_APPEND:
        pass
        
    elif state == S3_PLOT:
        print (x_axis)
        print (y_axis)
        
        fig = pyplot.figure()
        ax = fig.add_axes([0.18, 0.1, .75, 0.8])
        ax.plot(x_axis[0],y_axis[0], 'k^')
        ax.set_title('ME 405 Lab')
        ax.set_xlabel('Time [seconds]')
        ax.set_ylabel('Encoder Reading [ticks]')
        pyplot.show()
        state = S3_DISPLAY
    elif state == S3_DISPLAY:
        pass