from .api_call import api_call
from .device import Device
from .entity import Entity
from .zone import Zone


class Account(Entity):
    """An account within the Freedom Robotics API. Normally fetched from a :obj:`FreedomClient`
    and not intended to be manually instantiated by the user of the API.

    Args:
        _id (str): Account ID.
        _data (`dict`): Account data.
    """

    def _make_url(self):
        return "/accounts/{}".format(self._id)

    @property
    def company(self):
        """str: The company or organization of the account.
        """
        return self._data.get("company")

    def find_device(self, name=""):
        """:obj:`Device`: Finds a device by its name (i.e. the name set in the Freedom web app).
        Case-insensitive.
        If there are no matches, or there is more than one match, an exception will be thrown.

        Args:
            name (str): The name of the device.
        """

        devices = [device for device in self.devices if device.name.lower() == name.lower()]

        if len(devices) == 0:
            raise Exception("No device found")

        if len(devices) > 1:
            raise Exception("Multiple devices found")

        return devices[0]

    def create_device(self, name = "default", description = "", device_type = "", location = "", platform = "ros"):
        """:obj:`Device`: Creates a new device.

        Args:
            name (str): Device name.
            description (str): Device description.
            device_type (str): Device type.
            location (str): Device location.
            platform (str): Device platform.
        """

        response = api_call("POST", "/accounts/%s/devices" % (self._id), data = {
            "name": name,
            "description": description,
            "type": device_type,
            "location": location,
            "platform": platform,
        })

        if response and response.get("status") != "success":
            raise Exception("create device error: %s" % str(response))
            return

        return self.device(response.get("device"))

    def device(self, device_id):
        """:obj:`Device`: Fetch an device by its device ID (Dxxxxxxxxxxxx).

        Args:
            device_id (str): Device ID.
        """

        device_data = api_call("GET", "/accounts/%s/devices/%s" % (self._id, device_id))
        if not device_data:
            return None

        device = Device(device_data["device"], device_data)
        return device

    @property
    def devices(self):
        """:obj:`list` of :obj:`Device`: Fetch a list of all devices in the account.
        """
        result = api_call("GET", "/accounts/%s/devices" % self._id)
        if not result:
            return None
        return [Device(device_data["device"], device_data) for device_data in result]

    @property
    def zones(self):
        """:obj:`list` of :obj:`Zone`: Fetch a list of all zones in the account.
        """
        result = api_call("GET", "/accounts/%s/zones" % self._id)
        if not result:
            return None
        return [Zone(data['id'], data) for data in result]

    @property
    def email(self):
        """str: Account e-mail address.
        """
        return self._data.get("email")

    @property
    def features(self):
        """str: Account features.
        """
        return self._data.get("features")

    @property
    def last_seen(self):
        """float: Unix time the account was last seen.
        """
        return self._data.get("last_seen")

    @property
    def max_devices(self):
        """int: Maximum number of devices in the account.
        """
        return self._data.get("max_devices")

    @property
    def name(self):
        """str: Account name.
        """
        return self._data.get("name")
