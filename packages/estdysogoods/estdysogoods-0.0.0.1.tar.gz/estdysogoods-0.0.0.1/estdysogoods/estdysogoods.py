import socket
import time
from iqoptionapi.stable_api import IQ_Option


def edsg_server_data(IP,PORT,NUMBERCONNECT):
	servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servers.bind((IP,PORT))
	servers.listen(NUMBERCONNECT)

	while True:
	    clientsocket, address = servers.accept()
	    print(f"Connect:{address}:OK")

	    msg = "Connect Success!"
	    clientsocket.send(bytes(msg,"utf-8"))

	    while True:
	        msg = input("SERVER: ")
	        msg = msg
	        clientsocket.send(bytes(msg,"utf-8"))
def edsg_send_data_order_binary(API):
	while True:
		ID_ORDER,CURRENCY_ORDER,TYPE_ORDER,AMOUNT_ORDER,START_ORDER,END_ORDER,RTTIME_ORDER = API.edsg_get_option_open_by_other_pc()
		if ID_ORDER != None:
			API.del_option_open_by_other_pc(ID_ORDER)
			return [ID_ORDER,CURRENCY_ORDER,TYPE]


def edsg_receive_data(servers):
    while True:
        data_text = ''
        new_msg = True
        while True:
            msg = servers.recv(9999)
            if new_msg:
                new_msg = False
            data_text += msg.decode("utf-8")
            return data_text

def edsg_main_copytrade_user_binary(useriq,passiq,iphost,port):
	API = IQ_Option(useriq,passiq)
	API.connect()
	servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servers.connect((iphost, port))
	data_id1 = []
	data_id2 = []
	while True:
		data_order = edsg_receive_data(servers)
		data_id1 = [data_order]
		if str(data_id1[0]) == "Connect Success!":
			print("Connect Success!")
		if data_id1 != data_id2 and str(data_id1[0]) != "Connect Success!":
			res = (data_order.strip('][').split(', '))
			ID_ORDER       = int(res[0].strip("']['"))
			CURRENCY_ORDER = res[1]
			TYPE_ORDER	   = res[2]
			AMOUNT_ORDER   = int(res[3])
			RTTIME_ORDER   = res[-1]
			data_id2 = [ID_ORDER]
			API.buy(AMOUNT_ORDER,CURRENCY_ORDER.strip("''"),TYPE_ORDER.strip("''"),int(RTTIME_ORDER)-int(1))

def ip(ip,port,numberconnect):
	servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servers.bind((ip,port))
	servers.listen(numberconnect)
	return servers


def edsg_main_copytrade_master_binary(ip,port,numberconnect,useriq,passiq):
	servers = ip(ip,port)
	API = IQ_Option(useriq,passiq)
	API.connect()
	while True:
		master = edsg_server_data(servers,API)

def test(API):	
	print("OK")
	while True:
		ID_ORDER,CURRENCY_ORDER,TYPE_ORDER,AMOUNT_ORDER,START_ORDER,END_ORDER,RTTIME_ORDER = API.edsg_get_option_open_by_other_pc()
		if ID_ORDER != None:
			API.del_option_open_by_other_pc(ID_ORDER)
			return [ID_ORDER,CURRENCY_ORDER,TYPE_ORDER,AMOUNT_ORDER,RTTIME_ORDER]
			

def edsg_server_data(IP,API):
	
	clientsocket, address = servers.accept()
	print("Connect ip:",address[0],"Port",address[1],"OK")

	msg_wc = "Connect Success!"
	clientsocket.send(bytes(msg_wc,"utf-8"))
	while True:
	     msg = str(test(API))
	     msg = msg
	     clientsocket.send(bytes(msg,"utf-8"))

		 
			
			
def ip(port,numberconnect):
	servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servers.bind((socket.gethostname() ,port))
	servers.listen(numberconnect)
	return servers

def edsg_main_master_copytrade_binary(useriq,passiq):
	API = IQ_Option(useriq,passiq)
	API.connect()
	while True:
		test2 = edsg_server_data(servers,API)