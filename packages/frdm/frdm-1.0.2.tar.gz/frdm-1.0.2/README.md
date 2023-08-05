# freedom-python-client

A Python library for interfacing with the [Freedom REST API](https://docs.freedomrobotics.ai/reference#rest-api) in a Pythonic way, presenting Accounts, Devices, Alerts, and other objects as instances of Python classes. Currently only supports reading from the API ("GET" requests).

# Installation
```
$ sudo python3 setup.py install
```
(sorry only Python3 support for now (TODO: add Python2 support))

# API documentation

```
Open docs/freedom_client/index.html in your favorite browser.
```

# Simple API examples
## Instantiating the API

With a token and secret:
```
from freedom_client import FreedomClient
freedom = FreedomClient(token = "TXXX", secret = "Sxxx")
```

With a username and password:
```
from freedom_client import FreedomClient
freedom = FreedomClient(username = "your@email.com", password = "foo")
```

With a saved credentials file:
```
from freedom_client import FreedomClient
freedom = FreedomClient()
```

The file should be in `~/.freedom_credentials` and contain a JSON structure with `token` and `secret` fields, e.g. `{"token":"TXXX", "secret":"SXXX"}`.

## Manipulating accounts

Getting a list of accounts you have access to:
```
for account in freedom.accounts:
    print(account)
````

## Manipulating devices

Getting a list of devices in the first account you have access to:

```
for device in freedom.accounts[0].devices:
    print(device.name)
```

You can fetch a specific device by its ID:
```
device = freedom.accounts[0].device("Dxxxxxxxxxxxx")
```
or search for it by its name, assuming that name is unique:
```
device = freedom.accounts[0].find_device("myrobot")
```

## Getting data from devices

Getting the most recent value from a ROS topic:
```
device = freedom.accounts[0].find_device("myrobot")
print(device.last_data("/gps/fix"))
```

Getting full data from a time interval:
```
device = freedom.accounts[0].find_device("myrobot")

# fetch last 1000 s of data
for message in device.data("/gps/fix", start = time.time() - 1000, end = time.time()):
    print(message)
```

# Advanced API examples

See the demo\_.py files. (TODO: more data analysis demos.)


# Distribution

First you will need to have a local `~/.pypirc` file with the configurations for both Test PyPi and the production one. E.g.

```
[testpypi]
  username = __token__
  password = <request for original token>

[pypi]
  username = __token__
  password = <request for original token>
```

## Steps

* Publish to testpypi:

```
REPOSITORY=testpypi ./publish_to_pypi.sh
```

* Check that it's working properly:

```
pip install --index-url https://test.pypi.org/simple freedom_client
```

* Push to actual PyPi

```
REPOSITORY=pypi ./publish_to_pypi.sh
```