"""
Library to manage and use a MyStromSwitch
author : Valentin Sandoz, valentin.sandoz@students.hevs.ch
date : 30.01.2023
"""
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
        r = requests.get(f"{self.host}/api/v1/info", headers=headers)
        return r.json()

    def _request(self, path, params=None):
        """
        Util method to do a request to the switch's API
        :param path: Path of the requests after the hostname (http://example.com/{path})
        :param params: Dict of params to pass to the request
        :return: JSON response or content if not JSON
        """
        headers = {"Accept": "application/json"}
        r = requests.get(f"{self.host}/{path}", headers=headers, params=params)
        logger.debug(r.request.url)
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            return r.content

    def getState(self):
        """

        :return: the current state of the switch
        """
        return self._request("report")["relay"]

    def getTemp(self):
        """
        Get the temperature measured by the switch (not very accurate!)
        :return: temperature in celcius
        """
        # if self.version == 1:
        #    raise Exception("Version 1 of the Mystrom Switch has no temperature sensor")
        return requests.get(f"{self.host}/temp").json()["compensated"]

    def getPower(self):
        """
        Get the power of the switch
        :return: power in watts
        """
        return self._request("report")["power"]

    def toggle(self):
        """
        Toogle the switch
        :return: the new switch's state (
        """
        return self._request("toggle")

    def setState(self, state):
        logging.info(f"Relay {self.name} set to {state}")
        return self._request("relay", params={"state": (1 if state else 0)})