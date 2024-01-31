import os
import socket
import subprocess

localIP = ""
localPort = 4321
bufSize = 32

exec(open(os.getcwd() + "/jukebox.conf").read())
musicDir = MUSIC_DIRECTORY

cmd = 'echo "1" > /tmp/PlayNo'
subprocess.run([cmd], shell=True)

cmd = os.getcwd() + "/bluetooth.sh -c"
subprocess.run([cmd], shell=True)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

while(True):
	rec = UDPServerSocket.recvfrom(bufSize)
	data = rec[0].decode("utf-8")
	sourceIP  = rec[1]

	if data == "@":
		f = open("/tmp/BluetoothStatus", "r")
		sts = f.readline().strip()
		f.close()

		if sts == "Connected":
			cmd = os.getcwd() + "/bluetooth.sh -d"
			sts = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
			UDPServerSocket.sendto(str.encode(sts), sourceIP)
		elif sts == "Disconnected":
			cmd = os.getcwd() + "/bluetooth.sh -c"
			sts = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
			UDPServerSocket.sendto(str.encode(sts), sourceIP)
		else:
			UDPServerSocket.sendto(str.encode("Disconnected"), sourceIP)
	elif data == ">":
		f = open("/tmp/PlayNo", "r")
		no = int(f.readline().strip())
		f.close()
		cmd = "ls -1 " + musicDir + " | wc -l"
		total = int(subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8"))

		if no < total:
			no = no + 1
		else:
			no = 1

		f = open("/tmp/PlayNo", "w")
		f.write(str(no) + "\n")
		f.close()

		cmd = os.getcwd() + "/play.sh " + str(no)
		subprocess.run([cmd], shell=True)
		UDPServerSocket.sendto(str.encode("Playing " + str(no)), sourceIP)
	elif data == "<":
		f = open("/tmp/PlayNo", "r")
		no = int(f.readline().strip())
		f.close()
		cmd = "ls -1 " + musicDir + " | wc -l"
		total = int(subprocess.run([cmd], shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8"))

		if no > 1:
			no = no - 1
		else:
			no = total

		f = open("/tmp/PlayNo", "w")
		f.write(str(no) + "\n")
		f.close()

		cmd = os.getcwd() + "/play.sh " + str(no)
		subprocess.run([cmd], shell=True)
		UDPServerSocket.sendto(str.encode("Playing " + str(no)), sourceIP)
	elif data == "#":
		cmd = "systemctl --user restart jukebox-playAll.service"
		subprocess.run([cmd], shell=True)
		UDPServerSocket.sendto(str.encode("Playing All"), sourceIP)
