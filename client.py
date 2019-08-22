'''
Change the ip address to the one on which server file is running
run using command in linux : "python3 client.py"

enter sample to run the sample audio

'''

import socket
import pyaudio
import wave
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(("127.0.0.1", 5544))

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
while True:
	res=client_socket.recv(1024).decode()
	print(res)
	print("\n")
	sys.stdout.flush()
	x=input("Enter The song to be Played : ")
	client_socket.send(x.encode())
	ch=int(client_socket.recv(1024).decode())
	if ch==0:
		print("!!! Choose a legal song number !!!")
		continue
	if ch==1:
		print(" Track !!  ",x,"  !! Playing")
		data="1"
		while data != "":
			data = client_socket.recv(1024)
			stream.write(data)

stream.stop_stream()
stream.close()
p.terminate()
