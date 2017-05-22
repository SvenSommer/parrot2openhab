#!/usr/bin/env python
import requests
import json
from pprint import pformat  # here only for aesthetic
import datetime

openhab_host = 'openhabianpi'
openhab_port = '8080'


number_parameter = ['_air_temperature_gauge_valuescurrent_value','_battery_gauge_valuescurrent_value','_fertilizer_gauge_valuescurrent_value','_light_gauge_valuescurrent_value','_watering_soil_moisture_gauge_valuescurrent_value']
string_paramter = ['_fertilizerstatus_key','_sensor_firmware_updatefirmware_upgrade_available','_lightstatus_key','_air_temperaturestatus_key','_watering_automatic_wateringstatus_key']
date_parameter = ['_watering_soil_moisturepredicted_action_datetime_utc','last_sample_utc']
all_parameter = number_parameter + string_paramter + date_parameter

def send_status_to_openhab(key, value):
    #print key , "=", value


#    TODO: Datetime und Switch-Elemente werden momentan nicht an Openhab gesendet. Fehler: 400 Client Error: Bad Request for url: http://openhabianpi:8080/rest/items/FlowerPower__lightstatus_key/state
    if key in all_parameter:
        url = 'http://{host}:{port}/rest/items/FlowerPower_{key}/state'.format(host=openhab_host, port=openhab_port, key=key)

        if value == None:
            value = ""

        try:
            if key in number_parameter:
                converted_value = value
            elif key in string_paramter:
                converted_value = value
            elif key in date_parameter:
                converted_value = value[:-1] + '.000'


            response = requests.put(url, headers={'Content-Type': 'text/plain'}, data=json.dumps(converted_value))
            print datetime.datetime.now(), 'updated', url,'=', converted_value
            if response.status_code != requests.codes.ok:
                response.raise_for_status()
        except Exception ,e:
                print datetime.datetime.now(), "-Error-"
                print datetime.datetime.now(), 'updating', key , "=", converted_value
                print datetime.datetime.now(), e


def process_item(item, parent=''):
        for key,value in item.items():
                if type(value) in [basestring , unicode, bool, float, int] or value == None:
                        send_status_to_openhab(key=parent+key, value=value)
                elif type(value) == dict:
                        process_item(value, parent=parent+'_'+key)

print datetime.datetime.now(), "Request data from Parrot Cloud"
# Set your own authentication token
req = requests.get('https://api-flower-power-pot.parrot.com/garden/v1/status',
                   headers={'Authorization': 'Bearer QDEGEW2IlCepthisisnotavalidkeynwIUGx1sbFckRbx'})

data = req.json()

print datetime.datetime.now(), "Data from Parrot received -> sending to Openhab Rest Api..."


for location in data['locations']:
        process_item(location)
print datetime.datetime.now(), "Finished!"
