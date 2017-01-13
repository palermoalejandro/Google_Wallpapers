"""
	Servicio para guardar imagenes de google home como fondos de pantalla que se actualizan automaticamente

"""


from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import logging
import time
import shutil
import os
import sys
import requests
import json

global log = []


def delete_old_files(filecount,downloaded):
	global log
	if file_count > 0:
		#delete the least recent downloaded files
		x = len(downloaded) - file_count 
		if x > 0:
			for i in range(x-1):
				try:
					os.remove(downloaded[i])
					downloaded.pop(i)
				except:
					log.append('[ERROR]: imposible borrar archivo %s', downloadad[i])
 

def download_file(url, file_path):

	response = requests.get(url, stream=True)
	try :
		with open(file_path, 'wb') as out_file:
		    shutil.copyfileobj(response.raw, out_file)
		del response
		return True
	except:
		return False



def download_wallpaper(file_path,downloaded):
	req = requests.get('https://clients3.google.com/cast/chromecast/home')
	soup = BeautifulSoup(req.text, 'html.parser')
	scripts = soup.find_all('script')

	script = str(scripts[4])

	initpos = script.index('lh3.googleusercontent.com')
	aux = script[initpos:-1]
	#print(aux)
	
	finalpos = aux.index('\\u003')
	finalpos = finalpos + initpos - 1
	
	link = script[initpos:finalpos]
	link = link.replace("com\\", "com")	
	link = 'https://' + link + '=s1280-w1920-h1080-p-k-no-nd-mv'
	
	#print(link)
	#req2 = requests.get(link)
	file_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.png'


	if download_file(link, file_path + file_name):
		downloaded.append(file_path + file_name)

def main():
	#get config
	global log
	log.append('Service started: %s', )
	config_path = "./config.json"
	with open(config_path, 'r') as configfile:
		config = json.loads(configfile.read())
		filecount = config['FILECOUNT']
		file_path = config['FILE_PATH']
		sleep_time = config['SLEEP_TIME']
		log_path = config['LOG_PATH']

	downloaded = []	
	
	while(1):
		#get new wallpapers from google
		download_wallpaper(file_path, downloaded)

		#delete old wallpaper files
		delete_old_files(filecount, downloaded)

		#sleep until next loop
		time.sleep(sleep_time)



if __name__ == '__main__':
	main()


