import os
import serial
import time
import sys, termios, tty
import thread

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600
ser.timeout = 1		#non-block read

ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read       
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write


CREDBG    = '\33[41m'
CBLUEBG   = '\33[44m'
CEND      = '\33[0m'
CYELLOW = '\33[33m'
CRED    = '\33[31m'


def input_thread(L):
    raw_input()
    L.append(None)

def open():
	#global ser
	#ser = serial.Serial('/dev/ttyUSB0', 9200)  # open serial port
	ser.open()
	print("Connecting to " + str(ser.name))
	print("Successfully connected? " + str(ser.isOpen()))
	#ser.write(b'hello')
	#return ser.name

def bootStd():
	#L = []
	#thread.start_new_thread(input_thread, (L,))
	
	os.system('clear')
	print("Hold MODE then power on Cisco switch")
	time.sleep(1)
	data = ser.readline()
	waitfor("password-recovery")
	os.system('clear')
	print("Release MODE button now")
	waitfor("switch:")
	#ser.write("".encode())
	time.sleep(1)
	ser.write("flash_init\r".encode())
	print("Loading Flash...")
	#waitfor("MORE")
	#ser.write("\r".encode())
	while "switch:" not in data:
		#ser.write("\r".encode())
		time.sleep(0.05)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		if "MORE" in data:
			ser.write("\r".encode())
			print("Continuing...")
		if "RETURN" in data:
			ser.write("\r".encode())
			print("Continuing...")
	#waitfor("switch:")
	print("\nFlash done loading")
	#time.sleep(5)
	#os.system('clear')
	#print("DONE!")
	return

def wipeStd():
	files=[]
	#files2=[]
	os.system('clear')
	print("Reading files...")
	ser.write("dir flash:/\r".encode())
	data = ser.readline()
	while "switch:" not in data:
		time.sleep(0.005)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		if ("-rwx" in data) and (".bin" not in data) and ("multiple-fs" not in data):
			files.append(data)
	print
	#time.sleep(1)
	#print files[-44:]
	files = [e[45:-1] for e in files]
	
	print("Files found:")
	if len(files) != 0:
		for filen in files:
			print(" > "+filen)
		print
		yn=raw_input("Delete these files? [Y/n]: ")
		if yn != "n":
			for filen in files:
				print
				print(CRED + filen + CEND)
				yn="y" #raw_input("Delete File? [Y/n]: ")
				if yn != "n":
					filedel="delete flash:/" + filen + "\r"
					#print(filedel)
					ser.write(filedel.encode())
					#data = ser.readline()
					waitfor("(y/n)")
					ser.write("y\r".encode())
					waitfor("switch:")
			print("All files deleted")
			time.sleep(2)
		os.system('clear')
	else:
		print("No files to delete")
		time.sleep(2)
	print("Double Checking...")
	ser.write("dir flash:/\r".encode())
	data = ser.readline()
	while "switch:" not in data:
		time.sleep(0.005)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		if ("-rwx" in data) and (".bin" not in data) and ("multiple-fs" not in data):
			files.append(data)
	print
	#raw_input("Press enter to continue...")
	print("Done here")
	bc=raw_input("Boot Check?: (y/N)")
	if bc == "y":
		ser.write("boot\r".encode())
		waitfor("Press RETURN to get started")
	time.sleep(1)	
	return()
	

def bootRtr():
	os.system('clear')
	data = ser.readline()
	print("Waiting for boot to complete...")
	while "Router>" not in data:
		time.sleep(0.005)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		if "System Configuration Dialog" in data:
			print("The switch is already Resetted.")
			time.sleep(2)
			print("Exiting")
			time.sleep(1)
			return
		elif "BOOTTIME" in data:
			print("Continuing..")
			ser.write("\r".encode())
		elif "Upgrade ROMMON initialized" in data:
			print("Continuing..")
			ser.write("\r".encode())
	ser.write("enable\r".encode())
	time.sleep(1)
	ser.write("write erase\r".encode())
	waitfor("configuration")
	ser.write("\r".encode())
	waitfor("Router>")
	print("Rebooting...")
	ser.write("reload\r".encode())



def wipeASA():
	os.system('clear')
	data = ser.readline()
	print("Please Power on router")
	time.sleep(1)
	print("Waiting for boot to complete...")
	waitfor("ESC")
	print("Temporarily Overriding Password...")
	time.sleep(1)
	ser.write("\x1b".encode())
	time.sleep(1)
	waitfor("rommon")
	ser.write("confreg 0x41\r".encode())
	waitfor("rommon")
	print("Booting...")
	ser.write("boot\r".encode())
	#waitfor("asa>")
	while "asa>" not in data:
		time.sleep(0.005)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		if "configure Firewall" in data:
			print("The switch is already Resetted.")
			#time.sleep(2)
			ex=raw_input("Reset again? (Y/n)")
			if ex == "n":
				print("Exiting")
				time.sleep(1)
				return
			else:
				print("Going throough initial setup with bs")
				# try ctrl-c instead?
				waitfor("Firewall")
				ser.write("\r".encode())
				waitfor("password")
				ser.write("\r".encode())
				waitfor("recovery")
				ser.write("\r".encode())
				waitfor("Year")
				ser.write("\r".encode())
				waitfor("Month")
				ser.write("\r".encode())
				waitfor("Day")
				ser.write("\r".encode())
				waitfor("Time")
				ser.write("\r".encode())
				waitfor("IP")
				ser.write("192.168.1.1\r".encode())
				waitfor("mask")
				ser.write("255.255.255.0\r".encode())
				#waitfor("IP")
				#ser.write("192.168.1.2\r".encode())
				waitfor("Host")
				ser.write("host\r".encode())
				waitfor("Domain")
				ser.write("domain\r".encode())
				waitfor("IP")
				ser.write("192.168.1.2\r".encode())
				waitfor("save to flah")
				ser.write("no\r".encode())
				waitfor("Firewall")
				ser.write("no\r".encode())
				
				
				break
		if "Self-Test complete" in data:
			print("Continuing..")
			ser.write("\r".encode())
	

	ser.write("enable\r".encode())
	waitfor("Password")
	ser.write("\r".encode())
	waitfor("asa#")
	print("Erasing...")
	ser.write("write erase\r".encode())
	waitfor("Erase")
	ser.write("\r".encode())
	waitfor("asa#")
	ser.write("configure terminal\r".encode())
	waitfor("[Y]es")
	ser.write("N\r".encode())
	waitfor("(config)#")
	ser.write("config-register 0x01\r".encode())
	waitfor("(config)#")
	print("Saving...")
	ser.write("write\r".encode())
	waitfor("(config)#")
	rb=raw_input("Complete. Reboot and wipe HW module. (n/Y)")
	if rb != "n":
		ser.write("reload\r".encode())
		waitfor("confirm")
		ser.write("\r".encode())
		waitfor("ciscoasa>")
		ser.write("enable\r".encode())
		waitfor("Password")
		ser.write("\r".encode())
		waitfor("asa#")
		print("Erasing module...")
		ser.write("hw-module module 1 reset\r".encode())
		waitfor("confirm")
		ser.write("\r".encode())
		waitfor("asa#")
	print("Done. Exiting...")
	time.sleep(2)


def waitfor(case):
	data = ser.readline()
	print(CYELLOW + data + CEND),
	while case not in data:
		time.sleep(0.005)
		data = ser.readline()
		if len(data) > 0:
			print(CYELLOW + data + CEND),
		#if L:
		#	print("Exiting...")
		#	exit()
		#data = ser.readline()
	return()
		

def readtest():
	L = []
	thread.start_new_thread(input_thread, (L,))
	print("Press enter to exit readout....")
	time.sleep(2)
	while True:
		#print("Getting response...")
		data = ser.readline() 
		#data = ser.read(40)
		if len(data) > 0:
			print(data[:-1])
			

		time.sleep(0.005)
		if L:
			#print("yout pressed: " + str(L))
			print("Exiting...")
			return


def type():
	os.system('clear')
	print("Types:")
	print("  1) Cisco Catalyst Switch	(29xx - 37xx) 		")
	print("  2) Cisco router 		(2900)				(Beta)")
	print("  3) Cisco ASA 			(5515/5520)			(Beta)")
	print("  4) Cisco router 		(1800/1841)			(Dev)") #https://www.hardreset99.com/routers/cisco/cisco-1841-factory-reset/



	swtype = raw_input("Type: ")
	return swtype
	
os.system('clear')
#raw_input("Press enter to connect...") 
print("Connecting...")
open()

while True:
	swtype=type()	
	if swtype == "1":
		bootStd()
		wipeStd()
	elif swtype == "2":
		bootRtr()
	elif swtype == "3":
		wipeASA()
	else:
		print("Invalid Response")
		time.sleep(2)
		#break


	

ser.close()
exit()

