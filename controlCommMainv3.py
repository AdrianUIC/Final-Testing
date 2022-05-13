import serdes
import tcpModule
import time
from mobilityMovementCommandv3 import moveRover
import os
import RPi.GPIO as GPIO

while True:
    try:
        #monitor pi with GPIO
        LED_PIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(2)

        port, pack = moveRover.servoSetup()
        rc1, rc2 = moveRover.init_RoboClaw()

        HOST = '192.168.1.162'
        PORT = 2356

        #create serializer and reciever objects
        ser = serdes.deserializer()
        print('waiting to connect')
        recv = tcpModule.reciever(HOST, PORT)
        print('connection confirmed')
        angle1 = 1150 #850 note 850 all thw way left, 1450 all the way right
        angle2 = 1150 #2400, note same as above for turning
        angle3 = 1600 #1850, note 2000 for turnng left, 1200 for right
        angle4 = 3600 #3200, note 3900 for left, 3300 for right

        flang = angle1
        frang = angle2
        blang = angle3
        brang = angle4

        '''
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        time.sleep(2)

        #turn left:
        angle = 350
        flang = angle + angle1
        frang = angle + angle2
        blang = -1*angle + angle3
        brang = -1*angle + angle4

        moveRover.moveServos(port, pack, flang, frang, blang, brang)
        moveRover.moveServos(port, pack, flang, frang, blang, brang)
        moveRover.moveServos(port, pack, flang, frang, blang, brang)

        time.sleep(2)
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)
        '''

        '''
        rc2.BackwardM1(0x80, 40)
        print('extend')
        time.sleep(2)
        temp = rc1.ReadCurrents(0x80)
        print(repr(temp[1]))
        rc2.ForwardM1(0x80, 0)
        print('stop')
        '''



        #recieve messages
        print('will now recieve messages!')
        while True:
            
            msg = recv.recieve_msg()
            data = ser.decode(msg) #note that data is a python list that contains the different values
            print(data[0]) #contains the message type



            #do the stuff based on the data
            if data[0] == 'move':

                wheelVel = data[1]
                angle = data[2]
                #print(str(angle) +' '+str(wheelVel))
                print(str(angle))
                #print(type(angle))
                #print(type(wheelVel))

                #Move Wheels
                print(wheelVel)
                amps = moveRover.wheelMotors(rc1, wheelVel)

                #Move Servos
                flang = angle + angle1
                #print(flang)
                frang = angle + angle2
                #print(frang)
                blang = -1*angle + angle3
                #print(blang)
                brang = -1*angle + angle4
                #print(brang)
                moveRover.moveServos(port, pack, flang, frang, blang, brang)

            elif data[0] == 'mine':
                speed = 300
                digVel = data[4]
                print(digVel)
                moveRover.digMotor(rc1, digVel)

                if data[2]:
                    curr = moveRover.digActuator(rc2, speed)
                elif data[3]:
                    curr = moveRover.digActuator(rc2, -speed)
                else:
                    curr = moveRover.digActuator(rc2, 0)


            elif data[0] == 'dump':
                speed = 300
                if data[1]:
                    curr = moveRover.dumpActuator(rc2, speed)
                elif data[2]:
                    curr = moveRover.dumpActuator(rc2, -speed)
                else:
                    curr = moveRover.dumpActuator(rc2, 0)
                pass
            
            moveRover.moveServos(port, pack, flang, frang, blang, brang)

    except:
        pass
        #timer to reset
        #look up how to shut down
        #os.system('controlCommMainv3.py')

