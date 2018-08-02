import socket, subprocess, sys, os, time, string, re
from threading import Thread

HOST = ""
FORMATS = "Correct format: ./proxy [logOptions] srcPort server dstPort"
BUFFER =1024
logOptions = ""
srcPort = 0
dstHost = ""
dstPort = 0


class ClientThread(Thread): 
	def __init__(self,connection,source,destination): 
		Thread.__init__(self)
		self.conn =  connection
		self.s = source 
		self.d = destination 

	def run(self): 
		try:
			while True:
				data = conn.recv(BUFFER)
				if logOptions == "-raw":
					print("---> " + data.decode('utf-8'))
				elif logOptions == "-strip":
					output = ''
					for x in data.decode('utf-8'):
						if x in string.printable:
							output.join(x)
						else:
							output.join('.')
					print("---> " + output)
				elif logOptions == "-hex":
					print("---> " + data.decode("hex"))
				elif "-auto" in logOptions:
					try:
						legth = int(logOptions.replace("-auto", ""))
						if not (32 <= legth <= 127):
							
					except Exception:
						print("logOption has a wrong format: " + logOptions)
				self.d.send(data) 
				receive = self.d.recv(BUFFER)
				if logOptions == "-raw":
					print("---> " + receive.decode('utf-8'))
				elif logOptions == "-strip":
					output = ''
					for x in receive.decode('utf-8'):
						if x in string.printable:
							output.join(x)
						else:
							output.join('.')
					print("---> " + output)
				elif logOptions == "-hex":
					print("---> " + receive.decode("hex"))

				self.s.send(receive)
				if not receive:
					print ("Done with the connection")
					self.d.close()
					self.s.close()
					break
		except Exception as e:
			print("Client Closed With Exception:" + e)


def initial():
	if len(sys.argv) == 3:
		try:
			srcPort = int(sys.argv[1])
			dstHost = sys.argv[2]
			dstPort = int(sys.argv[3])
		except Exception:
			print("Make sure the format is correct:")
			print(FORMATS)
	elif len(sys.argv) == 4:
		try:
			logOptions = sys.argv[1]
			srcPort = int(sys.argv[2])
			dstHost = sys.argv[3]
			dstPort = int(sys.argv[4])
		except Exception:
			print("Make sure the format is correct:")
			print(FORMATS)
	else:
		print("The number of argument is not correct!")
		print(FORMATS)
		return False
	print("Port logger running: srcPort=" + srcPort + " host=" + dstHost + " dstPort=" + dstPort)
	return True

def listenForConnection():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, srcPort))

	print("Listening connection on port", PORT)
	s.listen(10)
	thread = []

	while True:
		conn, addr = s.accept()
		print ("New connection: "+ time.strftime("%c") + ", from "+  addr)
		d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		d.connect((dstHost, dstPort))
		
		newthread = ClientThread(conn,s,d) 
		newthread.start() 
		threads.append(newthread)

def main():
	if initial() == True:
		listenForConnection()

if __name__ == '__main__':
	main()