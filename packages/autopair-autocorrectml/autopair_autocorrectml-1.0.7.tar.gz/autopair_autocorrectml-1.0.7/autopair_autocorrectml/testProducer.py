from kafka import KafkaProducer
import json
import sys
import argparse
import logging

class QueryProducer():
	def __init__(self,serverUrl,checkTopic):
		self.serverUrl = serverUrl
		self.checkTopic = checkTopic
		
	def send(self,sampleDict):
		producer = KafkaProducer(bootstrap_servers=self.serverUrl)
		sampleJsonByte = json.dumps(sampleDict, indent=2, sort_keys=True).encode()
		producer.send(self.checkTopic,sampleJsonByte)
		logging.info('Sent ' + str(sampleDict) + ' to ' + self.serverUrl)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--server', default = 'localhost:9092')
	parser.add_argument('-m', '--mode', default = 'python')
	parser.add_argument('-c', '--check', default = 'product.correction.check.topic')
	
	args = parser.parse_args()
	serverUrl = args.server
	mode = args.mode
	checkTopic = args.check
	
	logging.basicConfig(
		format='%(asctime)s (%(name)s) %(levelname)s: %(message)s',
		level=logging.INFO
	)
	
	logging.getLogger("kafka").setLevel(logging.CRITICAL)
	logging.getLogger("akka").setLevel(logging.CRITICAL)
	
	sender = QueryProducer(serverUrl,checkTopic)
	
	sampleDict = {
		'carBrand': 'โตโญต้า',
		'carModel': 'แคมรี่',
		'carNickname': '-',
		'itemName': 'ลูกหมาคันชัก',
		'itemFitment': 'ซ้าย, ขวา',
		'itemBrand': 'มี๋',
		'itemUnit': 'อัน',
	}
	
	#sampleDict = {
	#	 'carBrand': 'TOYOTA',
	#	 'carModel': 'CAMRY',
	#	 'carNickname': '-',
	#	 'itemName': 'ลูกหมากแร็ค',
	#	 'itemFitment': 'ซ้าย',          
	#	 'itemBrand': '333',
	#	 'itemUnit': 'อัน',
	#}
	
	sender.send(sampleDict)