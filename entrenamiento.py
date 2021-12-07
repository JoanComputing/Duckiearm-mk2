import sys
sys.path.append('/home/pi/mlf/core')
sys.path.append('/home/pi/duckietown/Duckiearm-mk2/')
from serial_control import SerialControl
#from core.serial_control import SerialControl #for pc
import time
from Transfromacion import *
import csv

camera = VideoCamera(flip=False)

robot_serial = SerialControl()
robot_serial.open_serial()

# angulos maximos motores
# m1: 0 - 90  	base
# m2: 90 - 160 	brazo vertical
# m3: 90 - 50 	brazo horizontal
m1_min = 0
m1_max = 90
m1_step = 10
m2_min = 90
m2_max = 160
m2_step = 10
m3_min = 50
m3_max = 80
m3_step = 10

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

with open('datos.csv', 'w', newline='') as file:
    writer = csv.writer(file, dialect = 'excel')
    writer.writerow(['X', 'Y', 'Z', 'U', 'V', 'Theta1', 'Theta2', 'Theta3'])
    

    for t1 in range(m1_min,m1_max,m1_step):
      robot_serial.write_servo(1,t1)
      '''
      u = int(input("u: "))
      v = int(input("v: "))
      r = int(input("r: "))
      x,y,z = TransFinal(u,v,r)
      #with open('datos.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([x, y, z, u, v, t1, t2, t3])
      '''
      for t2 in range(m2_min,m2_max,m2_step):
          robot_serial.write_servo(2,t2)
          '''
          u = int(input("u: "))
          v = int(input("v: "))
          r = int(input("r: "))
          x,y,z = TransFinal(u,v,r)
          #with open('datos.csv', 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow([x, y, z, u, v, t1, t2, t3])
          '''
          for t3 in range(m3_min, m3_max, m3_step):
              robot_serial.write_servo(3, t3)
              '''
              u = int(input("u: "))
              v = int(input("v: "))
              r = int(input("r: "))
              '''
              time.sleep(2)
              u,v,r = detectarCirculo(camera)
              if u is not None:
                x,y,z = TransFinal(u,v,r)
                x=np.round(x,1)
                y=np.round(y,1)
                z=np.round(z,1)
                print(x,y,z)
              else:
                x = None
                y = None
                z = None
               # with open('datos.csv', 'w', newline='') as file:
              writer.writerow([t1, t2, t3, u, v, r, x, y, z])
  
              print("m1: "+str(t1)+" m2: "+str(t2)+" m3: "+str(t3))
              

robot_serial.read_status()
#robot_serial.read_sensors()
#robot_serial.run_effector()

robot_serial.close_serial()

