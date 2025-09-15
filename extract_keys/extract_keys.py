#!/usr/bin/env python3

import sys
import requests
import urllib3
import getpass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADER = {'Content-Type': 'application/json'}

if (len(sys.argv)!=2):
	print ("\nusage:-")
	print ("./client_show <CipherTrust_URL>")
	quit()
else:
	ct_url = sys.argv[1]
	ct_username = input("Username : ")
	ct_password = getpass.getpass("Password : ")
	ct_domain = input("Domain : ")


def ct_login():
	global jtoken
	url = ct_url+"/api/v1/auth/tokens"
	post_data = {"name": ct_username, "password": ct_password, "domain": ct_domain}

	response = requests.post(url, headers=HEADER, verify=False, json=post_data)
	if(response.status_code!=200):
		print("Failed to login")
		quit()

	jtoken = response.json()["jwt"]
	print(" --> Login success")



def ct_list_keys():
	global keys
	HEADER = {'Authorization': 'Bearer '+jtoken}
	url = ct_url+"/api/v1/vault/keys2"
	response = requests.get(url, headers=HEADER, verify=False)
	no_of_keys = response.json()['total']
	if(no_of_keys==0):
		print(" --> There are no keys to export")
		quit()

	param = {"limit": no_of_keys}
	response = requests.get(url, headers=HEADER, verify=False, params=param)
	keys = response.json()['resources']
	print(" --> ",no_of_keys, "keys found")


def ct_extract_key(key_id):
	url = ct_url + "/api/v1/vault/keys2/" + key_id + "/export"
	HEADER = {'Authorization': 'Bearer '+ jtoken, "accept": "application/json"}
	response = requests.post(url, headers=HEADER, verify=False)
	raw_key = response.json()
	return raw_key


def ct_delete_key(key_id):
	url = ct_url + "/api/v1/vault/keys2/" + key_id
	HEADER = {'Authorization': 'Bearer '+ jtoken, "accept": "application/json"}
	response = requests.delete(url, headers=HEADER, verify=False)
	if(response.status_code!=204):
		print("Failed to delete", key_id, ".Status : ",response.status_code)


ct_login()
ct_list_keys()
extracted_keys = 0
with open("raw_keys.dat", "a") as fWrite:
	for key in keys:
		if(key['unexportable'] == False):
			raw_key = ct_extract_key(key['id'])
			fWrite.write(raw_key["name"] + ", " + raw_key["material"] + "\n")
			extracted_keys += 1
		#ct_delete_key(key['id'])
fWrite.close()

print (" --> ", extracted_keys, "keys extracted successfully")
