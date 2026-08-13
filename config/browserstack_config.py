import os


BROWSERSTACK_USERNAME = os.getenv(
    "BROWSERSTACK_USERNAME"
)

BROWSERSTACK_ACCESS_KEY = os.getenv(
    "BROWSERSTACK_ACCESS_KEY"
)


BROWSERSTACK_CAPABILITIES = {
    "browser": "Chrome",
    "deviceName": "Samsung Galaxy S22",
    "realMobile": True,
    "os": "android",
    "osVersion": "12",
}
