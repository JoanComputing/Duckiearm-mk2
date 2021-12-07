import sys
sys.path.append('/home/pi/mlf/core')
from serial_control import SerialControl
#from core.serial_control import SerialControl #for pc
import time

robot_serial = SerialControl()
robot_serial.open_serial()

# angulos maximos motores
# m1: 0 - 90  	base
# m2: 90 - 160 	brazo vertical
# m3: 90 - 50 	brazo horizontal
m1_min = 0
m1_max = 90
m1_step = 15
m2_min = 90
m2_max = 160
m2_step = 15
m3_min = 50
m3_max = 90
m3_step = 15

'''
for i in range(6):
    t1 = -i*20
    t2 = 10*i+90
    t3 = -10*i+90
    robot_serial.write_servo(1,t1)
    robot_serial.write_servo(2,t2)
    robot_serial.write_servo(3,t3)
    print("m1: "+str(t1)+" m2: "+str(t2)+" m3: "+str(t3))
    time.sleep(1)
'''
'''
for t1 in range(m1_min,m1_max,m1_step):
    robot_serial.write_servo(1,t1)
    for t2 in range(m2_min,m2_max,m2_step):
        robot_serial.write_servo(2,t2)
        for t3 in range(m3_min, m3_max, m3_step):
            robot_serial.write_servo(3, t3)
            print("m1: "+str(t1)+" m2: "+str(t2)+" m3: "+str(t3))
            time.sleep(1)
            '''
robot_serial.write_servo(2,120)

while(1):
  pass
robot_serial.read_status()
#robot_serial.read_sensors()
#robot_serial.run_effector()

robot_serial.close_serial()

