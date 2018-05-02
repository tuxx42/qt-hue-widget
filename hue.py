import requests
import sys
import random
import json
import os


TMPFILE = '/tmp/hue.lock'
base = 'http://192.168.1.42'


class Hue:
    STATE_OFF = False
    STATE_ON = True

    def __init__(self, username):
        self.username = username

    def get_lights(self):
        url = '{}/api/{}/lights'.format(base, self.username)
        try:
            res = requests.get(url)
            return res.json()
        except Exception as e:
            print(e)

    def get_light(self, light):
        url = '{}/api/{}/lights/{}'.format(base, self.username, light)
        try:
            res = requests.get(url)
            return res.json()
        except Exception as e:
            print(e)

    def set_light_state(self, light, state, bri=None):
        url = '{}/api/{}/lights/{}/state'.format(
            base, self.username, light)

        data = {'on': state}
        if bri:
            data.update({'bri': bri})

        try:
            res = requests.put(url, data=json.dumps(data))
        except Exception as e:
            print(e)

        print(res.json())

    def set_relative_brightness(self, light, state, bri=None):
        res = self.get_light(light)
        bri = res['state']['bri'] + bri
        if bri <= 0:
            self.set_light_state(light, self.STATE_OFF)
        else:
            self.set_light_state(light, state, bri)


def randTrue():
    return random.choice([True, False])


if __name__ == '__main__':
    hue = Hue(username='lUwwJ1eMFb59iG5pANwAAw0VhTaG9UJxWvHMekTv')
    state = True if sys.argv[2] in ['1', 'true', 'True', 'on'] else False

    if os.path.exists(TMPFILE):
        print('bailing')
        sys.exit(0)

    try:
        open(TMPFILE, 'w').close()
        bri = int(sys.argv[3])
        if sys.argv[4][0] in ['-', '+']:
            hue.set_relative_brightness(sys.argv[1], state=state, bri=bri)
        else:
            hue.set_light_state(sys.argv[2], state=state, bri=bri)
    finally:
        print('removing')
        os.unlink(TMPFILE)
