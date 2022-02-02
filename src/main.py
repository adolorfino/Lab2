'''
    @file       lab2main.py
    @brief      Main file is designed to give tasks.
    @details    This file does not deal with the hardware directly but 
                assigns task to the task_user.py and task_encoder.py files. 
                Task to individual encoders can be assigned here and parameters
                like period, the rate at which the encoder responds, can
                be controlled here as well.

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: January 10, 2022
'''

import task_encoder,motor_driver, closedloop, shares, pyb, utime
from pyb import USB_VCP
vcp = USB_VCP()

def main():
    ''' 
    @brief      The main program
    @details    Tasks for the individual motors, encoders, and the user interface
                is established here, as well as the data that these tasks 
                collectively share.
    ''' 
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_1 =  shares.Share(0)
    delta_pos_1 =shares.Share(0)
    enc_zero_1 = shares.Share(False)
    enc_duty_1=  shares.Share(0)
    
    ## @brief   A variable enable that is true whenever there is not a fault.
    ## @details This variable is written in task_user.py and is set to True
    ##          if the 'c' key is pressed to reset the fault condition.
    enable = shares.Share()
    
    ## @brief   A variable fault_found that triggers during a fault.
    ## @details This variable is written in DRV8847.py and is set to True
    ##          if a fault is detected.
    fault_found = shares.Share(False)
    
    printout = []
    times = []
    
    
    
    e_pin_1 = pyb.Pin.cpu.B6
    e_pin_2 = pyb.Pin.cpu.B7
    e_channel = 4
    
    m_pin_1 = pyb.Pin.board.PB4
    m_pin_2 = pyb.Pin.board.PB5
    m_enable = pyb.Pin.board.PA10
    m_timer = pyb.Timer(3, freq = 20000)
    
    task1 = task_encoder.Task_Encoder(65535, e_channel,enc_pos_1, delta_pos_1,enc_zero_1, e_pin_1, e_pin_2)
    task2 = motor_driver.MotorDriver(m_enable, m_pin_1, m_pin_2, m_timer)
    task3 = closedloop.ClosedLoop(0, 8192, 1,enc_pos_1)
    try:
        reference_time = utime.ticks_ms()
        current_time = utime.ticks_ms()
        difference = utime.ticks_diff(current_time, reference_time)
        while difference <= 1000:
            current_time = utime.ticks_ms()
            difference = utime.ticks_diff(current_time, reference_time)
#             enc_zero_1.write(True)
            task1.run()

            task3.set_Kp(.1)
#             task3.set_location(enc_pos_1.read())
            duty = task3.run()
            task2.set_pwm(duty)
            printout.append(enc_pos_1.read())
            times.append(difference)
#             utime.sleep_ms(5)
        return [printout, times]
    except MemoryError:
        print('done')
    except KeyboardInterrupt:
        return [printout, times]
        
        
if __name__ == '__main__':
    [x,y] = main()
    for n in range(0,len(x),1):
        auteur = str(y[n])+', '+str(x[n])
        vcp.write(auteur.encode())
        vcp.write('\n')
#         utime.sleep_ms(50)
    vcp.write('end'.encode())