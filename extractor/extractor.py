from Crypto.Util.number import *
import base64
import binascii
import os
import re

file_list = os.listdir(".")
suffix = ".encrypted"
len_suffix = len(suffix)

encrypted_file_list = []
for I in file_list:
	if I[-len_suffix:] == suffix:
		encrypted_file_list.append(I)

Main_KEY = "jBA+5BeYHByhRJZQx0ueEBvQPGuTYvGqxVNf3SuAch2T5/e/pb10DVFawre/eupwifyCzP4zTbiqFFs9vjI6ZStrv4CHnPrPL6hkpe7Apy+Mqfju/X7qGHs8WLW6NEhSOMWJnUZE+YJ4UprOrRD7cYMUU6aJ/XaJsE3wAQMXUt0lHm69hbdhz6dLl3RJ5RhOPCzlSKGNWRLYZXkHD2Vv2WJUiwQhMdLxQhUfd6ZyF0fEgDavRAg1mfQ86kf0Cb9U9wclyKizZBjg/PW4NZDaOyDzOEUB87rlBWXfzJh7Hf/n10OUEvs5AVzucdznLixzqh/WzuEZoj4L7tQjB4G4sQ=="
Main_RSA_n = 18461090511526494635680046089239911506582300448626881063830286038674865652783677024404293738678094212847547547457166471135492764422082854574133502325088817564614902648045539104101815287573218866088294414838961195968474193865414756152616434018063043282100025282389589552426871973306643932112713322426244034286383859635930292449783916320363306991656169643845016783071779181067359502011218907150938073150434398468282966556087934165438089239862856178140399744182514709857990974726101003114382533227994179033507725844701607500151684788922402605171926057790318786106279294985164731956599181078807132058577967175719374466651
Main_RSA_e = 65537
key = bytes_to_long(base64.b64decode(Main_KEY))
for I in encrypted_file_list:
	tmp_file = open(I, "rb")
	byte_data = tmp_file.read()
	tmp_file.close()
	key_set = re.findall(".*?:.*?:.*?:", byte_data.decode("ISO-8859-1"))[0]
	key_set = key_set.split(":")
	TMP_PUBKEY = bytes_to_long(base64.b64decode(key_set[0]))
	TMP_PRIKEY = pow(bytes_to_long(base64.b64decode(key_set[1])), key, Main_RSA_n)
	test = getPrime(1024)
	if test == pow(pow(test, Main_RSA_e, TMP_PUBKEY), TMP_PRIKEY, TMP_PUBKEY):
		print("%s: %s" % (I, base64.b64encode(long_to_bytes(TMP_PRIKEY)).decode()))
	else:
		print("%s: %s" % (I, "Can't extract TMP_PRIKEY"))