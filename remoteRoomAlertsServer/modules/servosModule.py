import Adafruit_PCA9685
class Servos:

   # servo settings
   servo_min = 150 
   servo_max = 600
   increment = 10

   def __init__(self):
      # Set servos to starting position
      self.horizontalPosition = 400
      self.verticalPosition = 350
      # setting up the servos
      self.pwm = Adafruit_PCA9685.PCA9685() # configures I2C communication with servo hat
      self.pwm.set_pwm_freq(60)
      self.pwm.set_pwm(14,0,self.horizontalPosition)
      self.pwm.set_pwm(15,0,self.verticalPosition)

   def moveServo(self, direction):     
      if (direction == "L"):
         if (self.horizontalPosition < Servos.servo_max):
            self.horizontalPosition += Servos.increment
            self.pwm.set_pwm(14,0,self.horizontalPosition)
      elif (direction == "R"):
         if (self.horizontalPosition > Servos.servo_min):
            self.horizontalPosition -= Servos.increment
            self.pwm.set_pwm(14,0,self.horizontalPosition)
      elif (direction == "U"):
         if (self.verticalPosition > Servos.servo_min):
            self.verticalPosition -= Servos.increment
            self.pwm.set_pwm(15,0,self.verticalPosition)
      elif (direction == "D"):
         if (self.verticalPosition < Servos.servo_max):
            self.verticalPosition += Servos.increment
            self.pwm.set_pwm(15,0,self.verticalPosition)

