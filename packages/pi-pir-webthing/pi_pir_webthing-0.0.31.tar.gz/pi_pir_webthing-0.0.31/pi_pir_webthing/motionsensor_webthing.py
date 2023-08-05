from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import RPi.GPIO as GPIO
from datetime import datetime
import tornado.ioloop


class MotionSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number, name, description):
        Thing.__init__(
            self,
            'urn:dev:ops:motionSensor-1',
            'Motion ' + name + ' Sensor',
            ['MotionSensor'],
            description
        )

        self.gpio_number = gpio_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)
        GPIO.add_event_detect(self.gpio_number, GPIO.BOTH, callback=self.__update, bouncetime=5)
        self.is_motion = False

        self.motion = Value(False)
        self.add_property(
            Property(self,
                     'motion',
                     self.motion,
                     metadata={
                         '@type': 'MotionProperty',
                         'title': 'Motion detected',
                         "type": "boolean",
                         'description': 'Whether ' + name  + ' motion is detected',
                         'readOnly': True,
                     }))

        self.last_motion = Value(datetime.now().isoformat())
        self.add_property(
            Property(self,
                     'motion_last_seen',
                     self.last_motion,
                     metadata={
                         'title': 'Motion last seen',
                         "type": "string",
                         'unit': 'datetime',
                         'description': 'The ISO 8601 date time of last movement',
                         'readOnly': True,
                     }))
        self.ioloop = tornado.ioloop.IOLoop.current()

    def __update(self, channel):
        if GPIO.input(self.gpio_number):
            logging.info("motion detected")
            self.ioloop.add_callback(self.__update_motion_prop, True)
        else:
            self.ioloop.add_callback(self.__update_motion_prop, False)

    def __update_motion_prop(self, is_motion):
        if is_motion:
            self.motion.notify_of_external_update(True)
            self.last_motion.notify_of_external_update(datetime.now().isoformat())
        else:
            self.motion.notify_of_external_update(False)


def run_server(hostname, port, gpio_number, name, description):
    motion_sensor = MotionSensor(gpio_number, name, description)
    server = WebThingServer(SingleThing(motion_sensor), hostname=hostname, port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


