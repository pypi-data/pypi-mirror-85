# ------------------------------------------------------------------------------
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0 
# ------------------------------------------------------------------------------
# Demonstrates how to call/orchestrate AWS fleet provisioning services
#  with a provided bootstrap certificate (aka - provisioning claim cert).
#   
# Initial version - Raleigh Murch, AWS
# email: murchral@amazon.com
# ------------------------------------------------------------------------------


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from axon.config_loader import Config
import logging
import json
import os
import asyncio
import glob
import time
import uuid
from pkg_resources import resource_filename

# Set Config path
CONFIG_PATH = resource_filename('axon', 'config.ini')
# Set Certs path
CERTS_PATH = resource_filename('axon', 'certs')


class IoTService:

	def __init__(self, write_key=None, device_info={}):
		"""Initializes the IoT service
		
		Arguments:
			file_path {string} -- path to your configuration file
		"""
		# Logging
		logging.basicConfig(level=logging.ERROR)
		self.logger = logging.getLogger(__name__)

		# Load configuration settings from config.ini
		self.write_key = write_key
		# Store tracking type and other device metadata
		self.device_info = device_info
		self.config = Config(CONFIG_PATH)
		self.config_parameters = self.config.get_section('SETTINGS')
		self.secure_cert_path = CERTS_PATH
		self.iot_endpoint = self.config_parameters['IOT_ENDPOINT']
		self.template_name = self.config_parameters['PRODUCTION_TEMPLATE']
		self.rotation_template = self.config_parameters['CERT_ROTATION_TEMPLATE']
		self.claim_cert = self.config_parameters['CLAIM_CERT']
		self.secure_key = self.config_parameters['SECURE_KEY']
		self.root_cert = self.config_parameters['ROOT_CERT']
		self.ownership_token = None

		# Determine if dev env
		self.is_dev = 'axon-provisioning-develop' in self.config_parameters['PRODUCTION_TEMPLATE']

		# Create unique client ID
		if 'CLIENT_ID' in self.config_parameters:
			self.client_id = self.config_parameters['CLIENT_ID']
		else:
			self.client_id = str(uuid.uuid4())
			# Persisted in register_thing_callback()

		# self.client_id = str(int(round(time.time() * 1000)))

		# ------------------------------------------------------------------------------
		#  -- PROVISIONING HOOKS EXAMPLE --
		# Provisioning Hooks are a powerful feature for fleet provisioning. Most of the
		# heavy lifting is performed within the cloud lambda. However, you can send
		# device attributes to be validated by the lambda. An example is show in the line
		# below (.hasValidAccount could be checked in the cloud against a database).
		# Alternatively, a serial number, geo-location, or any attribute could be sent.
		#
		# -- Note: This attribute is passed up as part of the register_thing method and
		# will be validated in your lambda's event data.
		# ------------------------------------------------------------------------------

		self.primary_MQTTClient = AWSIoTMQTTClient(self.client_id)
		self.test_MQTTClient = AWSIoTMQTTClient(self.client_id)
		self.primary_MQTTClient.onMessage = self.on_message_callback
		self.callback_returned = False
		self.message_payload = {}
		self.isRotation = False
		self.is_connected = False

	def core_connect(self):
		""" Method used to connect to connect to AWS IoTCore Service. Endpoint collected from config.
		
		"""
		# Was if isRotation is True:
		if self.get_current_certs():
			self.logger.info('##### CONNECTING WITH EXISTING CERT #####')
			print('##### CONNECTING WITH EXISTING CERT #####')
		else:
			self.logger.info('##### CONNECTING WITH PROVISIONING CLAIM CERT #####')
			print('##### CONNECTING WITH PROVISIONING CLAIM CERT #####')

		self.primary_MQTTClient.configureEndpoint(self.iot_endpoint, 8883)
		self.primary_MQTTClient.configureCredentials("{}/{}".format(self.secure_cert_path,
														self.root_cert), "{}/{}".format(self.secure_cert_path, self.secure_key),
														"{}/{}".format(self.secure_cert_path, self.claim_cert))
		self.primary_MQTTClient.configureOfflinePublishQueueing(-1)
		self.primary_MQTTClient.configureDrainingFrequency(2)
		self.primary_MQTTClient.configureConnectDisconnectTimeout(10)
		self.primary_MQTTClient.configureMQTTOperationTimeout(3)

		self.primary_MQTTClient.connect()

		# Future: Confirm connection using subscription to topic "$aws/events/presence/connected/<client_id>"
		self.is_connected = True

	def core_disconnect(self):
		self.primary_MQTTClient.disconnect()

	def core_publish(self, data):
		topic = self.device_topic()
		# If device topic is empty, accountID and deviceID have not yet been set. Return
		# if len(topic) == 0: return
		# topic = self.client_id
		self.primary_MQTTClient.publish(topic, json.dumps(data), 1)
		print("Published: '" + json.dumps(data) + "' to the topic: " + topic)

	def get_current_certs(self):
		non_bootstrap_certs = glob.glob('{}/[!boot]*.crt'.format(self.secure_cert_path))
		non_bootstrap_key = glob.glob('{}/[!boot]*.key'.format(self.secure_cert_path))

		# Get the current cert
		if len(non_bootstrap_certs) > 0:
			self.claim_cert = os.path.basename(non_bootstrap_certs[0])

		# Get the current key
		if len(non_bootstrap_key) > 0:
			self.secure_key = os.path.basename(non_bootstrap_key[0])

		return len(non_bootstrap_certs) > 0 and len(non_bootstrap_key) > 0

	def certs_exist(self):
		non_bootstrap_certs = glob.glob('{}/[!boot]*.crt'.format(self.secure_cert_path))
		non_bootstrap_key = glob.glob('{}/[!boot]*.key'.format(self.secure_cert_path))

		# Get True if certs and key exist, False if they do not
		return len(non_bootstrap_certs) > 0 and len(non_bootstrap_key) > 0

	def enable_error_monitor(self):
		""" Subscribe to pertinent IoTCore topics that would emit errors
		"""
		self.primary_MQTTClient.subscribe(
			"$aws/provisioning-templates/{}/provision/json/rejected".format(self.template_name),
			1,
			callback=self.basic_callback
		)
		self.primary_MQTTClient.subscribe("$aws/certificates/create/json/rejected", 1, callback=self.basic_callback)

	async def get_official_certs(self, isRotation=False):
		""" Initiates an async loop/call to kick off the provisioning flow.

			Triggers:
			   on_message_callback() providing the certificate payload
		"""
		if isRotation:
			self.template_name = self.rotation_template
			self.isRotation = True

		return await self.orchestrate_provisioning_flow()

	async def orchestrate_provisioning_flow(self):
		# Connect to core with provision claim certs
		self.core_connect()

		# Monitor topics for errors
		self.enable_error_monitor()

		# Make a publish call to topic to get official certs
		self.primary_MQTTClient.publish("$aws/certificates/create/json", "{}", 0)

		# Subscribe to Register Thing response at this stage in the provisioning lifecycle
		# (before bootstrap credentials get switched out)
		print('##### SUBSCRIBING TO REGISTER THING RESPONSE #####')
		provisioning_response_topic = "$aws/provisioning-templates/{}/provision/json/accepted".format(self.template_name)
		self.primary_MQTTClient.subscribe(provisioning_response_topic, 1, callback=self.register_thing_callback)

		# Wait the function return until all callbacks have returned
		# Returned denoted when callback flag is set in this class.
		while not self.callback_returned:
			await asyncio.sleep(0)

		return self.message_payload

	def on_message_callback(self, message):
		""" Callback Message handler responsible for workflow routing of msg responses from provisioning services.
		
		Arguments:
			message {string} -- The response message payload.
		"""
		json_data = json.loads(message.payload)

		# A response has been received from the service that contains certificate data.
		if 'certificateId' in json_data:
			self.logger.info('##### SUCCESS. SAVING KEYS TO DEVICE! #####')
			print('##### SUCCESS. SAVING KEYS TO DEVICE! #####')
			self.assemble_certificates(json_data)

		# A response contains acknowledgement that the provisioning template has been acted upon.
		elif 'deviceConfiguration' in json_data:
			if self.isRotation:
				self.logger.info('##### ACTIVATION COMPLETE #####')
				print('##### ACTIVATION COMPLETE #####')
			else:
				self.logger.info('##### CERT ACTIVATED AND THING {} CREATED #####'.format(json_data['thingName']))
				print('##### CERT ACTIVATED AND THING {} CREATED #####'.format(json_data['thingName']))

			self.validate_certs()
		else:
			self.logger.info(json_data)

	def assemble_certificates(self, payload):
		""" Method takes the payload and constructs/saves the certificate and private key. Method uses
		existing AWS IoT Core naming convention.
		
		Arguments:
			payload {string} -- Certifiable certificate/key data.

		Returns:
			ownership_token {string} -- proof of ownership from certificate issuance activity.
		"""
		# Cert ID
		cert_id = payload['certificateId']
		self.new_key_root = cert_id[0:10]

		self.new_cert_name = '{}-certificate.pem.crt'.format(self.new_key_root)
		# Create certificate
		f = open('{}/{}'.format(self.secure_cert_path, self.new_cert_name), 'w+')
		f.write(payload['certificatePem'])
		f.close()

		# Create private key
		self.new_key_name = '{}-private.pem.key'.format(self.new_key_root)
		f = open('{}/{}'.format(self.secure_cert_path, self.new_key_name), 'w+')
		f.write(payload['privateKey'])
		f.close()

		# Store references to new certificates in config.ini
		self.config.set_section([{
			"key": "PROD_CERT",
			"value": self.new_cert_name
		}, {
			"key": "PROD_KEY",
			"value": self.new_key_name
		}])

		# Extract/return Ownership token
		self.ownership_token = payload['certificateOwnershipToken']

		# Register newly acquired certificate
		print("Registering Thing: " + self.client_id)
		self.register_thing(self.ownership_token)

	def register_thing(self, token):
		"""Calls the fleet provisioning service responsible for acting upon instructions within device templates.
		
		Arguments:
			token {string} -- The token response from certificate creation to prove ownership/immediate possession of the certs.
			
		Triggers:
			on_message_callback() - providing acknowledgement that the provisioning template was processed.
		"""
		if self.isRotation:
			self.logger.info('##### VALIDATING EXPIRY & ACTIVATING CERT #####')
			print('##### VALIDATING EXPIRY & ACTIVATING CERT #####')
		else:
			self.logger.info('##### CREATING THING ACTIVATING CERT #####')
			print('##### CREATING THING ACTIVATING CERT #####')

		# Provide parameters to provisioning template
		register_template = {
			"certificateOwnershipToken": token,
			"parameters": {
				"ProjectWriteKey": self.write_key,
				"TrackingType": self.device_info.get('tracking_type'),
				# Optionally, users can set a device name to connect to an existing record.
				# If they do not, devices are created automatically.
				"DeviceName": self.device_info.get('name')
			}
		}

		# Register thing / activate certificate
		print('##### REGISTERING THING #####')
		provisioning_topic = "$aws/provisioning-templates/{}/provision/json".format(self.template_name)

		self.primary_MQTTClient.publish(provisioning_topic, json.dumps(register_template), 0)

	def validate_certs(self):
		"""Responsible for (re)connecting to IoTCore with the newly provisioned/activated certificate - (first class citizen cert)
		"""
		self.logger.info('##### CONNECTING WITH OFFICIAL CERT #####')
		print('##### CONNECTING WITH OFFICIAL CERT #####')
		self.cert_validation_test()
		self.new_cert_pub_sub()
		print("##### ACTIVATED AND TESTED CREDENTIALS ({}, {}). #####".format(self.new_key_name, self.new_cert_name))
		print("##### FILES SAVED TO {} #####".format(self.secure_cert_path))

		# Finish provisioning flow
		self.test_MQTTClient.disconnect()
		self.callback_returned = True
		print("Provisioning complete!")

	def cert_validation_test(self):
		self.test_MQTTClient.configureEndpoint(self.iot_endpoint, 8883)
		self.test_MQTTClient.configureCredentials(
			"{}/{}".format(self.secure_cert_path, self.root_cert),
			"{}/{}".format(self.secure_cert_path, self.new_key_name),
			"{}/{}".format(self.secure_cert_path, self.new_cert_name)
		)
		self.test_MQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.test_MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.test_MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		self.test_MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
		self.test_MQTTClient.connect()

	def new_cert_pub_sub(self):
		"""Method testing a call to the device-specific topic (which was specified in the policy for the new certificate)
		"""
		topic = self.device_topic()
		# topic = self.client_id
		print("##### SUBSCRIBING TO TOPIC {} #####".format(topic))
		self.test_MQTTClient.subscribe(topic, 1, self.basic_callback)
		print("##### PUBLISHING TO TOPIC {} #####".format(topic))
		self.test_MQTTClient.publish(topic, str({"service_response": "##### RESPONSE FROM PREVIOUSLY FORBIDDEN TOPIC #####"}), 0)

	def switch_to_prod_certs(self):
		self.primary_MQTTClient.configureCredentials(
			"{}/{}".format(self.secure_cert_path, self.root_cert),
			"{}/{}".format(self.secure_cert_path, self.new_key_name),
			"{}/{}".format(self.secure_cert_path, self.new_cert_name)
		)

		# Set related properties to reference prod certs
		self.claim_cert = self.new_cert_name
		self.secure_key = self.new_key_name

	# CALLBACKS
	def basic_callback(self, client, userdata, msg):
		"""Method responding to the device-specific publish attempt. Demonstrating a successful pub/sub with new certificate.
		"""
		self.logger.info(msg.payload.decode())
		self.message_payload = msg.payload.decode()

	def register_thing_callback(self, client, userdata, message):
		json_data = json.loads(message.payload)

		print("##### REGISTER THING CALLBACK #####")
		device_config = json_data['deviceConfiguration']
		# Save values in device configuration file
		self.config.set_section([{
			"key": "DEVICE_ID",
			"value": device_config['deviceID']
		}, {
			"key": "ACCOUNT_ID",
			"value": device_config['accountID']
		}, {
			"key": "CLIENT_ID",
			"value": self.client_id
		}])
		# Update config_parameters variable
		self.config_parameters = self.config.get_section('SETTINGS')
		# Swap bootstrap certs in primary_MQTTClient for production certs
		self.switch_to_prod_certs()

		return message

	def on_connect_callback(self):
		print("##### CONNECTION WITH IOT CORE ESTABLISHED #####")
		self.is_connected = True

	# HELPERS
	def device_topic(self):
		if 'ACCOUNT_ID' in self.config_parameters and 'DEVICE_ID' in self.config_parameters:
			account_id = self.config_parameters['ACCOUNT_ID']
			device_id = self.config_parameters['DEVICE_ID']
			topic = "account/" + account_id + "/device/" + device_id
			if self.is_dev:
				topic = "dev/" + topic
			return topic
		else:
			return ""
