from corrector import Corrector
import numpy as np
import sys
import json
import logging
import multiprocessing
import argparse

from kafka import KafkaConsumer,KafkaProducer

class Consumer():
	def __init__(self,serverUrl,mode,checkTopic,replyTopic):
		self.c = Corrector()
		self.serverUrl = serverUrl
		self.mode = mode
		self.checkTopic = checkTopic
		self.replyTopic = replyTopic		
		self.run()
		
	def run(self):
		consumer = KafkaConsumer(bootstrap_servers=self.serverUrl)
		consumer.subscribe(self.checkTopic)
		logging.info('Consumer successfully initiated.')
		for message in consumer:
			byteValue = message.value
			reply_header = message.headers
			stringValue = byteValue.decode("utf-8")
			data = json.loads(stringValue)
			logging.info('Received ' + str(data))
			suggested_car_brand=self.c.query_car_brand(data['carBrand'])
			suggested_car_model=self.c.query_car_model(data['carModel'])
			suggested_car_name=self.c.query_item_name(data['itemName'])
			suggested_item_brand=self.c.query_item_brand(data['itemBrand'])
			suggested_item_fitment=self.c.query_fitment(data['itemFitment'])
			data['carBrand'] = suggested_car_brand['refined']
			data['carModel'] = suggested_car_model['refined']
			data['itemName'] = suggested_car_name['refined']
			data['itemBrand'] = suggested_item_brand['refined']
			data['itemFitment'] = suggested_item_fitment['refined']         
			data['corectionStatus'] = 'UPDATED' if any([suggested_car_brand['isDiff'],suggested_car_model['isDiff'],suggested_car_name['isDiff'],suggested_item_brand['isDiff'],suggested_item_fitment['isDiff']]) else 'FOUND'
			data['updatedInfo'] = list(np.array(['carBrand','carModel','itemName','itemBrand','itemFitment'])[np.array([suggested_car_brand['isDiff'],suggested_car_model['isDiff'],suggested_car_name['isDiff'],suggested_item_brand['isDiff'],suggested_item_fitment['isDiff']])==1])
			logging.info('Suggested ' + str(data))
			extracted = [data.copy() for i in range(len(data['itemFitment']))]
			[extracted[i].update({'itemFitment':d}) for i,d in enumerate(data['itemFitment'])]
			if mode == 'python':
				self.replyMessagePython(extracted,reply_header)
			else:
				self.replyMessageSpring(extracted,reply_header)
				
		consumer.close()
	def replyMessagePython(self,data,header):
		logging.debug(header)
		producer = KafkaProducer(bootstrap_servers=self.serverUrl)
		logging.debug('prepare send msg')
		outputByte = json.dumps(data, indent=2, sort_keys=True).encode()
		logging.debug(outputByte)
		producer.send(self.replyTopic,outputByte,headers = header)
		
	def replyMessageSpring(self,data,header):
		logging.debug(header)
		producer = KafkaProducer(bootstrap_servers=self.serverUrl)
		logging.debug('prepare send msg')
		outputByte = json.dumps(data, indent=2, sort_keys=True).encode()
		replyTuple = [item for item in header if 'kafka_replyTopic' in item]
		replyTopic = replyTuple[0][1].decode("utf-8")
		logging.debug(replyTopic)
		producer.send(replyTopic, value=outputByte, headers = header)
		
def main(serverUrl,mode,checkTopic,replyTopic):
	Consumer(serverUrl,mode,checkTopic,replyTopic)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--server', default = 'localhost:9092')
	parser.add_argument('-m', '--mode', default = 'python')
	parser.add_argument('-c', '--check', default = 'product.correction.check.topic')
	parser.add_argument('-p', '--reply', default = 'product.correction.reply.topic')	
	args = parser.parse_args()
	serverUrl = args.server
	mode = args.mode
	checkTopic = args.check
	replyTopic = args.reply

	logging.basicConfig(
		format='%(asctime)s (%(name)s) %(levelname)s: %(message)s',
		level=logging.INFO
	)
	logging.info('Initializing.')	
	
	logging.getLogger("kafka").setLevel(logging.CRITICAL)
	logging.getLogger("akka").setLevel(logging.CRITICAL)
	
	main(serverUrl,mode,checkTopic,replyTopic)