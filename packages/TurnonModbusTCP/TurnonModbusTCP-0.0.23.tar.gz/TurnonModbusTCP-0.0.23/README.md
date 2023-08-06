TurnonModbusTCP



Python3.X :  import TurnonModbusTCP



clear_print()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Clear the command line.


get_my_IP()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation:  Get your IP.


set_client()

	type: < Operation >
	request type: { ServerIP= [string] , ServerPORT= [int] }
	result type: {}

	Explanation: Set up for connect to Modbus server.


client_start()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Connect to Modbus server.


state()

	type: < Event >
	request type: { address= [int] }
	result type: { [int] }

	Explanation: Get Modbus's value.


state()

	type: < Event >
	request type: { address= [int] , ID= [int] }
	result type: { [bool] }

	Explanation: Get Modbus's value.


robot_control()

	type: < Operation >
	request type: { control_mode= [int] , data_X= [float] , data_Y= [float] , data_Z= [float] , data_Xrot= [float] , data_Yrot= [float] , data_Zrot= [float] , wait_for_robot_done = [bool(true)]}
	result type: {}

	Explanation:	Control Franka robot by Modbus.
					control_mode=0  : Just write the data into Modbus whith out moving.
					control_mode=1  : Write the data into Modbus then move.
					
					data_X, data_Y, data_Z				:  -1.5mm ~ 1.5mm
					data_Xrot, data_Yrot, data_Zrot		:  -359.9deg ~ 359.9deg 


robot_control_rotation()

	type: < Operation >
	request type: { control_mode= [int] , data_Xrot= [float] , data_Yrot= [float] , data_Zrot= [float] , wait_for_robot_done = [bool(true)] }
	result type: {}

	Explanation: 	Control Franka robot by Modbus.
					control_mode=0  : Just write the data into Modbus whith out moving.
					control_mode=1  : Write the data into Modbus then move.
					data_Xrot, data_Yrot, data_Zrot		:  -359.9deg ~ 359.9deg
	
	




