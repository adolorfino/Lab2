'''!
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
'''!

import task_encoder,motor_driver, closedloop, shares, pyb, utime

def main():
    '''! 
    @brief      The main program
    @details    Tasks for the individual motors, encoders, and the user interface
                is established here, as well as the data that these tasks 
                collectively share.
    '''! 
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_1 =  shares.Share(0)
    delta_pos_1 =shares.Share(0)
    enc_zero_1 = shares.Share(False)
    enc_duty_1=  shares.Share(0)
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_2 = shares.Share(0)
    delta_pos_2 = shares.Share(0)
    enc_zero_2 = shares.Share(False)
    enc_duty_2=shares.Share(0)
    
    ## @brief   A variable enable that is true whenever there is not a fault.
    ## @details This variable is written in task_user.py and is set to True
    ##          if the 'c' key is pressed to reset the fault condition.
    enable = shares.Share()
    
    
    printout = []
    times = []
    ## @brief   A variable fault_found that triggers during a fault.
    ## @details This variable is written in DRV8847.py and is set to True
    ##          if a fault is detected.
     
    fault_found = shares.Share(False)

    #task1 = task_user.Task_User(100000,enc_pos_1,enc_pos_2, delta_pos_1,delta_pos_2, enc_zero_1, enc_zero_2,enc_duty_1, enc_duty_2,enable, fault_found)
    task2 = task_encoder.Task_Encoder(65535,4,enc_pos_1, delta_pos_1,enc_zero_1, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)
    #task3 = task_encoder.Task_Encoder(65535,8,enc_pos_2, delta_pos_2,enc_zero_2, pyb.Pin.cpu.C6, pyb.Pin.cpu.C7)

    pin1 = pyb.Pin.board.PB4
    pin2 = pyb.Pin.board.PB5
    pin_enable = pyb.Pin.board.PA10
    timer = pyb.Timer(3, freq = 20000)
    task4 = motor_driver.MotorDriver(pin_enable, pin1, pin2, timer)
    loop = closedloop.ClosedLoop(0, 1000, 1)
    enc_zero_1 = True
    
    reference_time = utime.ticks_ms()
    while loop.get_error() >=50:
        enc_zero_1 = False
        
        # Establishes time value that will be constantly updated.
        current_time = utime.ticks_ms()
        # The calculated value of the difference between current and reference time.
        difference = utime.ticks_diff(current_time, reference_time)
        task2.run()
        try:
            loop.set_Kp(.1)
            loop.set_location(enc_pos_1.read())
            duty = loop.run()
            task4.set_pwm(duty)
            #loop.set_setpoint(enc_pos_1.read()+256)
            printout.append(enc_pos_1.read())
            times.append(difference)
        except ValueError:
            pass
        utime.sleep_ms(10)
        
    try:
        for x in range (100):
            print (times[x],printout[x])
    except IndexError:
        pass
        
if __name__ == '__main__':
    main()