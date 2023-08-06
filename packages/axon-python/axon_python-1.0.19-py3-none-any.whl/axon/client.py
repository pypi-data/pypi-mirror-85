import logging
import asyncio
from datetime import datetime, timezone
from six import string_types
from schema import Schema
from axon.iot_service import IoTService
from axon.config_loader import Config
import nest_asyncio
nest_asyncio.apply()

TRACKING_TYPES = ['location', 'temperature']
TRACKING_SCHEMA = {
    'location': Schema({'latitude': float, 'longitude': float}),
    'temperature': Schema(float)
}

class Client(object):
    """Create a new Axon client."""
    log = logging.getLogger('axon')

    def __init__(self, write_key=None, device_info={}, debug=False, on_error=None, is_registered=None):
        self.iot_service = IoTService(write_key, device_info)
        self.write_key = write_key
        self.device_info = device_info
        self.on_error = on_error
        self.debug = debug
        self.is_registered = is_registered
        self.auth_in_progress = False
        self.msg_queue = []

        # Validate configuration parameters, particularly the existence of the write_key.
        require('write_key', write_key, string_types)

        if debug:
            self.log.setLevel(logging.DEBUG)

    def track(self, tracking_type=None, data=None, interval=None):
        # Validate params
        require('tracking_type', tracking_type, TRACKING_TYPES)
        # Validate that data adheres to the corresponding tracking schema.
        require('data', data, TRACKING_SCHEMA[tracking_type])
        # Validate that interval is a number
        if interval:
            require('interval', interval, float)

        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

        # Create message object
        msg = {
            'tracking_type': tracking_type,
            'data': data,
            'timestamp': timestamp
        }

        def publish_message():
            # Publish MQTT message to Axon infrastructure
            self.iot_service.core_publish(msg)

        # Purge queue of messages that have been collected while provisioning is in progress
        def auth_complete():
            for message in self.msg_queue:
                self.iot_service.core_publish(message)
            self.msg_queue = []

        # Option 1: If provisioning is in progress, add message to a queue
        if self.auth_in_progress:
            self.msg_queue.append(msg)
        # Option 2: If device is already registered and provisioning is not in progress
        elif self.is_registered:
            publish_message()
        # Option 3: Begin device provisioning
        else:
            # Also add message to queue
            self.msg_queue.append(msg)
            # Check for existence of device credentials locally. On callback, publish message
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            # Authenticate the device with Axon infrastructure if needed. On completion, publish_message.
            self.iot_service.device_info = self.device_info
            self.iot_service.device_info['tracking_type'] = tracking_type
            task = loop.create_task(self.authenticate_if_needed(auth_complete))
            loop.run_until_complete(task)

        return msg

    # Disconnect from Axon IoT Infrastructure. In the future, this should flush any events stored offline as well.
    def shutdown(self):
        self.iot_service.core_disconnect()

    async def authenticate_if_needed(self, callback):
        if self.iot_service.get_current_certs():
            # TODO: Check if certs have expired and if so, rotate official certs
            # self.iot_service.get_official_certs(callback, isRotation=True)
            if not self.iot_service.is_connected:
                self.iot_service.core_connect()
                self.is_registered = True
            return callback()  # return True if certs exist
        else:
            # Await certificate provisioning result. Return on completion.
            self.auth_in_progress = True
            result = await self.iot_service.get_official_certs()
            self.auth_in_progress = False
            self.is_registered = True
            return callback()

    # Deleting (Calling destructor)
    # def __del__(self):
    #     self.iot_service.core_disconnect()
    #     print('Destructor called, Disconnect MQTT connection.')


# Helper methods
# def callback_function(payload):
#     # Return certs payload if certs are fetched during this step
#     return payload


def require(name, field, data_type):
    # Support custom data types. If data_type is an array, check field value must be contained in the array.
    if isinstance(data_type, list):
        if field not in data_type:
            msg = '{0} must be on of: {1}, got: {2}'.format(name, data_type, field)
            raise AssertionError(msg)
    # data_type is a schema object. Use Schema's provided validation.
    elif isinstance(data_type, Schema):
        data_type.validate(field)
    else:
        """Require that the named `field` has the right `data_type`"""
        if not isinstance(field, data_type):
            msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
            raise AssertionError(msg)
