# Script send sms alert when someone login to the linux instance as root.

## To run

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Install nexmo

https://developer.vonage.com/

Add following details:

```
NEXMO_KEY=yourkey
NEXMO_SECRET=yoursecret
TARGET_PHONE_NUMBER=yourphonenumber
TARGET_PHONE_NUMBER=yournexmosourcenumber
```
