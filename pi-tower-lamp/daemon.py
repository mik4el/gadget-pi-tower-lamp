import os
import requests
from datetime import datetime
import threading
import queue
import json


class DataAuther:
    def __init__(self, username, password, base_url):
        self.login_url = base_url + '/backend/api-token-auth/'
        self.username = username
        self.password = password
        self.token = None

    def auth_and_get_token(self):
        credentials = {'username': self.username, 'password': self.password}
        r = requests.post(self.login_url, json=credentials)
        self.token = r.json()['token']
        return self.token


class DataPosterWorker(threading.Thread):
    def __init__(self, token, base_url, data, status_queue):
        threading.Thread.__init__(self)
        gadget_slug = "pi-tower-lamp"
        self.post_url = base_url + '/backend/api/v1/gadgets/' + gadget_slug + '/data/'
        self.headers = {'Authorization': 'Bearer ' + token}
        self.data = data
        self.status_queue = status_queue

    def run(self):
        self.post_data(self.data)

    def update_status(self, message):
        self.status_queue.put(message)

    def post_data(self, data):
        payload = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        try:
            r = requests.post(self.post_url, json=payload, headers=self.headers)
        except:
            self.update_status("Error when posting.")
            return
        if r.status_code != 201:
            self.update_status(r.status_code)
            self.update_status(r.json())
            self.update_status("Request not ok when posting.")
        else:
            self.update_status("Posted: '{}'".format(data))


class PITowerLampRGBLED:
    def __init__(self, towerControllerQueue, lampControllerQueue):
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.lampModel = None
        self.pins = [2, 3, 4]
        self.redScaling = 1.0
        self.greenScaling = 0.3
        self.blueScaling = 0.1
        self.username = os.environ.get('GADGET_DATA_POSTER_USERNAME', None)
        self.password = os.environ.get('GADGET_DATA_POSTER_PASSWORD', None)
        self.base_url = os.environ.get('GADGET_DATA_POSTER_URL', '')
        self.status_queue = queue.Queue()

    def start(self):
        data_auther = DataAuther(self.username, self.password, self.base_url)
        token = data_auther.auth_and_get_token()

        while True:
            while not self.status_queue.empty():
                try:
                    message = self.status_queue.get()
                except queue.Empty:
                    pass
                else:
                    print("{:%Y-%m-%d %H:%M} {}".format(datetime.now(), message))
                    if message == "Request not ok when posting.":
                        # reauth
                        token = data_auther.auth_and_get_token()
                        print("Token updated.")
                        with self.status_queue.mutex:
                            self.status_queue.queue.clear()
            try:
                # Only redraw if new item in controllerQueue
                if not self.lampControllerQueue.empty():
                    self.lampModel = self.lampControllerQueue.get()
                    self.redraw()
                    if not self.towerControllerQueue.empty():
                        # avoid memory leak
                        tower_model = self.towerControllerQueue.get()
                        data = {"average_window_rgb": tower_model.averageWindowRGB, "all_windows_rgb": tower_model.allWindowsRGB}
                        data_poster = DataPosterWorker(token, self.base_url, data, self.status_queue)
                        data_poster.start()
                        del tower_model
            except KeyboardInterrupt:
                print("Exiting!")
                for p in self.pins:
                    os.system('echo "%d=0" > /dev/pi-blaster' % p)
                    os.system('echo "release %d" > /dev/pi-blaster' % p)
                exit()

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.set_light(self.lampModel.getRGB())
            else:
                self.set_light((0, 0, 0))

    def set_light(self, rgb):
        print("Setting", rgb)
        os.system(self.pi_blasterCommandForInput(self.pins[0], ((float(rgb[0]) / 255.0) * self.redScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[1], ((float(rgb[1]) / 255.0) * self.greenScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[2], ((float(rgb[2]) / 255.0) * self.blueScaling)))

    def pi_blasterCommandForInput(self, pin, value):
        return 'echo "%d=%.2f" > /dev/pi-blaster' % (pin, value)
