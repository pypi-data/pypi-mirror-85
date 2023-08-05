from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import RPi.GPIO as GPIO
import tornado.ioloop


class LightSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number, name, description):
        Thing.__init__(
            self,
            'urn:dev:ops:illuminanceSensor-1',
            'Illuminance ' + name + ' Sensor',
            ['MultiLevelSensor'],
            description
        )

        self.bright = Value(0)
        self.add_property(
            Property(self,
                     'brightness',
                     self.bright,
                     metadata={
                         '@type': 'BrightnessProperty',
                         'title': 'Brightness',
                         "type": "integer",
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                         'description': '"The level of light from 0-100',
                         'readOnly': True,
                     }))

        self.ioloop = tornado.ioloop.IOLoop.current()
        logging.info('bind to gpio ' + str(gpio_number))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_number, GPIO.IN)
        GPIO.add_event_detect(gpio_number, GPIO.BOTH, callback=self.__update, bouncetime=5)
        self.__update(gpio_number)

    def __update(self, gpio_number):
        if GPIO.input(gpio_number):
            self.ioloop.add_callback(self.__update_bright_prop, 0)
        else:
            self.ioloop.add_callback(self.__update_bright_prop, 100)

    def __update_bright_prop(self, brightness: int):
        self.bright.notify_of_external_update(brightness)
        logging.info("brightness: " + str(brightness))


def run_server(hostname:str, port: int, gpio_number: int, name: str, description: str):
    light_sensor = LightSensor(gpio_number, name, description)
    server = WebThingServer(SingleThing(light_sensor), hostname=hostname, port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
