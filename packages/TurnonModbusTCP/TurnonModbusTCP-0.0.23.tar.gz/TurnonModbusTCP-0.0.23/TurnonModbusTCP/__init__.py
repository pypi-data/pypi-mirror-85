import time
import pyModbusTCP
import argparse
import os
import sys
import socket
import platform

from pyModbusTCP.server import ModbusServer
from pyModbusTCP.client import ModbusClient

global modbus_host
global modbus_port
global localhost
global FrankaModebusTCPclient

global STATE


def MODBUS_STATE(STATE_NUMBER = 0):

        global STATE

        STATE = int(STATE_NUMBER)





def clear_print():

	if str(platform.system())=="Windows":
		os.system("cls")
	if str(platform.system())=="Linux":
		os.system("clear") 




def get_my_IP():
	
	while True:
		try:
			myname = socket.getfqdn(socket.gethostname())
			get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			get_s.connect(('8.8.8.8', 0))
			ip = ('hostname: %s, localIP: %s') % (myname, get_s.getsockname()[0])
			return get_s.getsockname()[0]

		except OSError:
			for i in range(4):
				
				strd = ""
				run=["~","\\","|","/"]
				for j in range(3):
					strd+="."

					for k in range(4):

						clear_print()

						print("getIP() : OSError: [Errno 101] Network is unreachable")
						print(" "+ run[k] +" Connected "+ strd)
						time.sleep(0.15)


def set_client(ServerIP="192.168.0.5",ServerPORT=502):
	global modbus_host
	global modbus_port

	modbus_host = ServerIP
	modbus_port = ServerPORT

	print("set_client:IP: "+modbus_host+" port: "+str(modbus_port))

	return modbus_host,modbus_port


def client_start():
	global FrankaModebusTCPclient

	FrankaModebusTCPclient = ModbusClient(host=modbus_host, port=modbus_port,auto_open=True, auto_close=True)
	'''
	clear_print()
	print(" ====================================")
	print("       Franka Modbus TCP Client  ")
	print(" ====================================")
	print(" Server IP: "+ modbus_host +"   Port: "+ str(modbus_port) )
	print(" ====================================")
	print("")
	'''
	print("start modbus client")
	time.sleep(1)

	while True: 
		try:
			regs_list= FrankaModebusTCPclient.read_holding_registers(9001, 1)
			operation = regs_list[0]
			print(" Connected...  Success")
			'''
			clear_print()
			print(" ====================================")
			print("       Franka Modbus TCP Client  ")
			print(" ====================================")
			print(" Server IP: "+ modbus_host +"   Port: "+ str(modbus_port) )
			print(" ====================================")
			print("")
			print("")
			print(" Connected...  Success")
			'''
			break
		except TypeError:
			for i in range(4):
				
				strd = ""
				run=["~","\\","|","/"]
				for j in range(3):
					strd+="."

					for k in range(4):

						clear_print()
						print(" ====================================")
						print("       Franka Modbus TCP Client  ")
						print(" ====================================")
						print(" Server IP: "+ modbus_host +"   Port: "+ str(modbus_port) )
						print(" ====================================")
						print("")
						print("") 						
						print("  Unable to connect to Host")
						print("")
						print("Please make sure the Host's settings are correct")
						print(" "+ run[k] +" Connected "+ strd)
						time.sleep(0.15)
			print("start client fail")

def client(ServerIP="auto_get_IP", ServerPORT=502, use_global=True):

        if ServerIP == "auto_get_IP":
                ServerIP=get_my_IP()
                print("client: auto_get_IP: "+ ServerIP)

        if use_global == True:

                global FrankaModebusTCPclient

                set_client(ServerIP,ServerPORT)
                client_start()
                return FrankaModebusTCPclient
        else:
                ModbusClient = ModbusClient(host=ServerIP, port=ServerPORT,auto_open=True, auto_close=True)
                return ModbusClient

def server(ServerIP="auto_get_IP", ServerPORT=502, no_block=True):
        
        if ServerIP == "auto_get_IP":
                ServerIP=get_my_IP()
                print("server: auto_get_IP: "+ ServerIP)

        # parse args
        parser = argparse.ArgumentParser()
        parser.add_argument('-H', '--host', type=str, default=ServerIP, help='Host')
        parser.add_argument('-p', '--port', type=int, default=ServerPORT, help='TCP port')
        args = parser.parse_args()
        # start modbus server
        server = ModbusServer(host=args.host, port=args.port, no_block=no_block)
        print("server start")
        server.start()
        return server
        
        
def state(address=-403, ID=-1):
	
	if address == -403 and ID == -1 :
		
		while True:

			try:
				data_list8 = FrankaModebusTCPclient.read_holding_registers(8001, 8)
				data_list9 = FrankaModebusTCPclient.read_holding_registers(9001, 8)
				data = data_list8[0]
				data = data_list9[0]
				print("")
				print("")
				print("--------------------------")
				print("   Franka Modbus state")
				print("--------------------------")
				print(" 8001: " + str(data_list8[0]) + "	" + " 9001: " + str(data_list9[0]))
				print(" 8002: " + str(data_list8[1]) + "	" + " 9002: " + str(data_list9[1]))
				print(" 8003: " + str(data_list8[2]) + "	" + " 9003: " + str(data_list9[2]))
				print(" 8004: " + str(data_list8[3]) + "	" + " 9004: " + str(data_list9[3]))
				print(" 8005: " + str(data_list8[4]) + "	" + " 9005: " + str(data_list9[4]))
				print(" 8006: " + str(data_list8[5]) + "	" + " 9006: " + str(data_list9[5]))
				print(" 8007: " + str(data_list8[6]) + "	" + " 9007: " + str(data_list9[6]))
				print(" 8008: " + str(data_list8[7]) + "	" + " 9008: " + str(data_list9[7]))
				print("")
				print("")
				return True
				break

			except TypeError:
				print("ERROR: state(): Connection to modbus server failed")
				return False
		

	elif address > 0 and address <= 9999 :

		if ID == -1 :

			while True:

				try:
					data_list = FrankaModebusTCPclient.read_holding_registers(address, 1)
					data = data_list[0]
					return data
					break

				except TypeError:
					print("ERROR: state(): Connection to modbus server failed")
					MODBUS_STATE(1)
					time.sleep(1)

		elif ID >= 1 and ID <= 16 :
			
			while True:

				try:
					data_list = FrankaModebusTCPclient.read_holding_registers(address, 1)
					data = data_list[0]
					fillBinData = '{:016b}'.format(data)
					data_bin = (str(fillBinData))[::-1]
					ID_data = bool(int(data_bin[ID-1:ID]))
					return ID_data
					break

				except TypeError:
					print("ERROR: state(): Connection to modbus server failed")
					MODBUS_STATE(1)
					time.sleep(1)
		
		
		else :
			print("ERROR: state(): ID value is out of range (1~16)")



	else:

		print("ERROR: state(): address value is out of range")



def Read(read_address=-1):
	if read_address > 0 and read_address <= 9999 : 
		return state(read_address)
	else:
		print("ERROR: Read(): Address is out of range")
		MODBUS_STATE(3)




def Write(write_address=-1, write_data=0):
	
	if write_address > 0 and write_address <= 9999 and write_data >= 0 and write_data <= 65535:

		errorsum = 0

		while True:

			FrankaModebusTCPclient.write_single_register(write_address,write_data)

			if state(write_address) == write_data :
				break

			else :


				if errorsum > 5 :
					break
				strd = ""
				run=["~","\\","|","/"]
				for j in range(3):
					strd+="."

					for k in range(4):

						clear_print()
						print("")
						print("WARNING: Write(): Sending failed")
						print(" "+ run[k] +" Resending ("+ str(errorsum) +")"+ strd)
						time.sleep(0.15)
				errorsum = errorsum +1
				


	elif write_address <= 0 or write_address > 9999 :
		
		print("")
		print("ERROR: Write(): Sending failed")
		print("       Write(): address is out of range")
		
	elif write_data < 0 or write_data > 65535 :

		print("")
		print("ERROR: Write(): Data is out of range")
		print("       Write(): Sending failed")
	else:
		print("")
		print("ERROR: Write(): Sending failed")






def rotation_check_and_write(data_Xrot, data_Yrot, data_Zrot):
        
        if data_Xrot != 3001 :

                if data_Xrot >= 0 and data_Xrot < 360:
                        Write(8006, int(data_Xrot*10) )

                elif data_Xrot < 0 and data_Xrot >= -360:
                        Write(8006, int(data_Xrot*10 + 3600) )

        if data_Yrot != 3001:

                if data_Yrot >= 0 and data_Yrot < 360:
                        Write(8007, int(data_Yrot*10) )

                elif data_Yrot < 0 and data_Yrot >= -360:
                        Write(8007, int(data_Yrot*10 + 3600) )

        if data_Zrot != 3001 :

                if data_Zrot >= 0 and data_Zrot < 360:
                        Write(8008, int(data_Zrot*10) )

                elif data_Zrot < 0 and data_Zrot >= -360:
                        Write(8008, int(data_Zrot*10 + 3600) )






def robot_control(control_mode=66, data_X=3001, data_Y=3001, data_Z=3001, data_Xrot=3001, data_Yrot=3001, data_Zrot=3001, wait_for_robot_done=True):
	
        if control_mode == 1 :

                if data_X != 3001 :
                        Write(8003, int(data_X*10000+15000) )
                if data_Y != 3001 :
                        Write(8004, int(data_Y*10000+15000) )
                if data_Z != 3001 :
                        Write(8005, int(data_Z*10000+15000) )

                rotation_check_and_write(data_Xrot, data_Yrot, data_Zrot)


                Write(9008, 86)
                time.sleep(0.1)

                times = 0
                while times < 10 :

                        if Read(9002) == 86 :

                                Write(9008, 1)
                                time.sleep(0.2)

                        if Read(9002) == 1 :

                                Write(9008, 66)

                                break

                        print("WARNING: robot_control(): Wait for Franka to respond")
                        time.sleep(1) 
                        times+=1

                        if times >= 10 :
                                print("")
                                print("ERROR: robot_control(): Franka did not respond")
                                return False

                if wait_for_robot_done == True:

                        while Read(9002) == 1:
                                time.sleep(0.1)


                Write(9008, 66)


        elif control_mode == 0 :


                if data_X != 3001 :
                        Write(8003, int(data_X*10000+15000))
                if data_Y != 3001 :
                        Write(8004, int(data_Y*10000+15000))
                if data_Z != 3001 :
                        Write(8005, int(data_Z*10000+15000))
                        
                rotation_check_and_write(data_Xrot, data_Yrot, data_Zrot)
                
                Write(9008, 0)

def robot_control_rotation(control_mode=66, data_Xrot=3001, data_Yrot=3001, data_Zrot=3001, wait_for_robot_done=True):
        if control_mode == 1 :
                rotation_check_and_write(data_Xrot, data_Yrot, data_Zrot)
                Write(9008, 86)
                time.sleep(0.1)

                times = 0
                while times < 10 :

                        if Read(9002) == 86 :
                                Write(9008, 1)
                                time.sleep(0.2)

                        if Read(9002) == 1 :
                                Write(9008, 66)
                                break
                        print("WARNING: robot_control(): Wait for Franka to respond")
                        time.sleep(1)
                        times+=1
                        if times >= 10 :
                                print("")
                                print("ERROR: robot_control(): Franka did not respond")
                                return False

                if wait_for_robot_done == True:
                        while Read(9002) == 1:
                                time.sleep(0.1)
                Write(9008, 66)
        elif control_mode == 0 :
                rotation_check_and_write(data_Xrot, data_Yrot, data_Zrot)
                Write(9008, 0)



'''

server()
client()

print(Read(8000))

Write(8000,123)

print(Read(8000))

robot_control(0, 0.5, 0.4, 0.3, 25, 35,-8)

state()


'''









         












