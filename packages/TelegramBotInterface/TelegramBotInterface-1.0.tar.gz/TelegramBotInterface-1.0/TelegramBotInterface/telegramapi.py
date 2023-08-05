################
# GPL-3.0-only #
################

import json
import requests

class TelegramAPI:
	def __init__(self, TOKEN):
		self.TOKEN = TOKEN
		self.URL = 'https://api.telegram.org/bot' + TOKEN + '/'

	def Update(self):
		resp = requests.get(self.URL+'getUpdates')
		r_json = resp.content.decode('utf8')
		r_dict = json.loads(r_json)
		return r_dict

	def readLastMessage(self):
		msg = self.Update()
		i = len(msg['result']) - 1
		#print(msg.keys())
		m_text = msg['result'][i]['message']['text']
		m_fname = msg['result'][i]['message']['from']['first_name']
		m_lname = msg['result'][i]['message']['from']['last_name']
	
		data = {'message': m_text, 'fromName': m_fname, 'fromLastName': m_lname}
		return data

	def getMe(self):
		r = requests.get(self.URL+'getMe')
		r_json = r.content.decode('utf8')
		r_dict = json.loads(r_json)
		data = r_dict['result']
		return data

	def sendMessage(self, chat_id, message):
		requests.get(self.URL+'sendMessage?text='+message+'&chat_id='+chat_id)


	def getCommands(self):
		r = requests.get(self.URL+'getMyCommands')
		r_json = r.content.decode('utf8')
		r_dict = json.loads(r_json)
		data = []
		#print(r_dict['result'])
		for l in r_dict['result']:
			data.append('/' + l['command'] + ' - ' + l['description'] + '\n')
		return data

	def sendDice(self, chat_id):
		r = requests.get(self.URL+'sendDice?chat_id='+chat_id)
		

