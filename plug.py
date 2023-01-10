import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyStromSwitch:
    """""
    Classe permettant d'obtenir les données depuis une MyStromSwitch et d'envoyer des action sur le relais.
    """

    def __init__(self, name, host=None, macAddress=None, version=2):
        self.name = name
        if macAddress is None and host is None:
            raise TypeError("MyStromSwitch() got no host nor macAddress. You must set only one of those")

        elif macAddress is not None and host is not None:
            raise TypeError("MyStromSwitch() got both host and macAddress. You must set one of those")

        elif macAddress is not None:
            if len(macAddress) == 6:
                parsed_mac = macAddress
            elif len(macAddress) == 17:
                parsed_mac = "".join(macAddress.split(":")[3:6])
            else:
                raise TypeError("The MAC address you set is not valid")
            self.host = f"http://mystrom-switch-{parsed_mac}.hevs.ch"

        elif host is not None:
            self.host = host

        try:
            self._get_version()
        except requests.exceptions.ConnectionError as exc:
            raise requests.exceptions.ConnectionError(f"{exc}\n\nImpossible to connect to the switch, verifiy your "
                                                      f"parameters and the switch")

        self.version = version

    def _get_version(self):
        headers = {"Accept": "application/json"}
        r = requests.get(f"{self.host}/api/v1/info")
        return r.json()

    def _request(self, path, params=None):
        headers = {"Accept": "application/json"}
        r = requests.get(f"{self.host}/{path}", headers=headers, params=params)
        logger.debug(r.request.url)
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            return r.content

    def getState(self):
        return self._request("report")["relay"]

    def getTemp(self):
        # if self.version == 1:
        #    raise Exception("Version 1 of the Mystrom Switch has no temperature sensor")
        return requests.get(f"{self.host}/temp").json()["compensated"]

    def getPower(self):
        return self._request("report")["power"]

    def toggle(self):
        return self._request("toggle")

    def setState(self, state):
        logging.info(f"Relay {self.name} set to {state}")
        return self._request("relay", params={"state": (1 if state else 0)})