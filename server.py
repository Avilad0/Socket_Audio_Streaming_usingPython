'''
store all file to play in the "resource" sub directory where the server file exists
run using command in linux : "python3 server.py"
the audio should be of .wav format with 44100 Hz frequency
'''

import socket
import pyaudio
import wave
import os
from _thread import *

def clientthread(conn,address):
	print("<",address , ">  connected ")
	while True:

		resource=os.listdir("./resource")
		ss="\n\n\n\n \t\t Media Player \n"
		for i in range(len(resource)):
			if i%2==0:
				ss+="\n"
			resource[i]=resource[i][:-4]
			ss=ss+"\t"+resource[i]+"\t"
		conn.send(ss.encode())
		x=conn.recv(1024).decode()
		for i in resource:
			if x.lower()==i.lower():
				print("song found")
				conn.send("1".encode())
				x=i
				break
		else:
			conn.send("0".encode())
			continue
		x="./resource/"+x+".wav"
		print(x)
		wf = wave.open(x, 'rb')
		
		p = pyaudio.PyAudio()
		
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        output=True,
		        frames_per_buffer=CHUNK)
		
		data =1
		while data :
			data = wf.readframes(CHUNK)
			conn.send(data)




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 5544))
server_socket.listen(10)
while True:
	conn, address = server_socket.accept()
	start_new_thread(clientthread,(conn,address))
