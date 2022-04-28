import serdes
import tcpModule
from mobilityMovementCommand import moveRover

port, pack = moveRover.servoSetup()
cont = moveRover.init_Roboteq()

HOST = '192.168.1.162'
PORT = 2356

#create serializer and reciever objects
ser = serdes.deserializer()
recv = tcpModule.reciever(HOST, PORT)
angle1 = 850
angle2 = 2400
angle3 = 1850
angle4 = 3200

moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)

#recieve messages
while True:
    try:
        msg = recv.recieve_msg()
        data = ser.decode(msg) #note that data is a python list that contains the different values
        print(data[0]) #contains the message type

        #do the stuff based on the data
        if data[0] == 'move':

            wheelVel = data[1]
            angle = data[2]
            print(str(angle) +' '+str(wheelVel))
            print(type(angle))
            print(type(wheelVel))
            #Move Wheels
            #amps = moveRover.wheelMotors(cont, wheelVel)

            #Move Servos
            angle1 = angle + 850
            angle2 = angle + 2400
            angle3 = -1*angle + 1850
            angle4 = -1*angle + 3200
            moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)

        elif data[0] == 'mine':
            speed = 300
            digVel = data[4]
            print(digVel)
            moveRover.digMotor(cont, digVel)
            if data[2]:
                curr = moveRover.digActuator(cont, speed)
            elif data[3]:
                curr = moveRover.digActuator(cont, -speed)
            else:
                curr = moveRover.digActuator(cont, 0)


        elif data[0] == 'dump':
            speed = 300
            if data[1]:
                curr = moveRover.dumpActuator(cont, speed)
            elif data[2]:
                curr = moveRover.dumpActuator(cont, -speed)
            else:
                curr = moveRover.dumpActuator(cont, 0)
            pass
        
        moveRover.moveServos(port, pack, angle1, angle2, angle3, angle4)

    except:
        pass
