'''@file                ClosedLoop.py
   @brief               ClosedLoop feedback control for the DC motors
   @details             A closed loop controller is used to reach desired motor location. The motor
                        takes the location of the motor, a specified setpoint of the motor, and uses
                        that information with a proportional gain to calculate a new duty cycle for
                        the motor such that the motor's location reaches the setpoint.
   @author              Aleya Dolorfino
   @author              Chloe Chou
   @author              Christian Roberts
   @date                February 5, 2022
'''

class ClosedLoop:
    '''
    @brief Close-loop controller class
    @details Close loop controller class to controll the speed of the motor 
    '''
    def __init__(self,location,setpoint,kp):
        '''
        @brief Object contructor for Closed Loop class
        @param delta This parameter is the measured motor velocity in rad/sec 
               omega_ref This parameter is the desired velocity in rad/sec inputed by the user
               kp This parameter is the proportional gain for the closeloop controller

        '''
        self.setpoint = setpoint
        self.location = location
        self.kp = kp
        
        
    def run(self):
        '''
        @brief Runs controller function 
        @details The function runs the closedloop feedback system. New calculated duty is below -100 or above 100
                 then the duty is set to the maximum duty of either -100 or 100. 
        @return duty This function returns the new calculated duty cycle for the DC motor 
        '''
        
        error = self.setpoint - self.location 
        self.duty = self.kp.read()*(error)
        
        if self.duty >100:
            self.duty = 100
        if self.duty <-100:
            self.duty = -100
        return self.duty
        
    def get_Kp(self,kp):
        '''
        @brief Method to retrieve the proportional controller gain value
        @param Stores the proportional gain kp inputed by the user 
        @returns The proportional gain kp
        '''
        return self.kp
     
    def set_Kp(self, kp):
        '''
        @brief Sets the controller gain value and allows modification for the controller gain value
        @param kp The proportional controller gain value

        '''
        self.kp = kp
        
    def get_setpoint(self):
        '''
        @brief Sets the controller gain value and allows modification for the controller gain value
        @param kp The proportional controller gain value

        '''
        return self.setpoint
        
    def set_setpoint(self, setpoint):
        '''
        @brief Sets the controller gain value and allows modification for the controller gain value
        @param kp The proportional controller gain value

        '''
        self.setpoint = setpoint