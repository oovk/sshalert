#!/usr/bin/env python

from concurrent.futures import process
import logging
import os, time
import subprocess, select
from urllib import response
import nexmo

log = logging.getLogger('sshalert')
log.setLevel(logging.INFO)

try:
    source_phone_number = os.getenv("SOURCE_PHONE_NUMBER")
    target_phone_number = os.getenv("TARGET_PHONE_NUMBER")
    nexmo_key = os.getenv("NEXMO_KEY")
    nexmo_secret = os.getenv("NEXMO_SECRET")
except:
    logging.critical("ERROR: Have you exported all required environment variables? (TARGET_PHONE_NUMBER, NEXMO_KEY, NEXMO_SECRET)")
    exit(1)

nexmo_client = nexmo.Client(key=nexmo_key, secret=nexmo_secret)

def poll_logfile(filename):
    f = subprocess.Popen(["tail", "-F", "-n", "0", filename], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    while True:
        if p.poll(1):
            process_log_entry(f.stdout.readline())
        time.sleep(1)

def process_log_entry(logline):
    if all(x in logline for x in ["sudo", "COMMAND"]):
        send_sms(logline)
    
    elif all(x in logline for x in ["ssh", "Accepted"]):
        send_sms(logline)
    return

def send_sms(msg):

    response = nexmo_client.send_message({
        'from': source_phone_number,
        'to': target_phone_number,
        'text':msg,
    })

    if response['message'][0]['status'] != 0:
        logging.error("ERROR: failed to send message: {0}".format[response['message'][0]['error-text']])
    else:
        logging.info("successfully sent text message")

if __name__ == "__main__":
    poll_logfile("/var/log/auth.log")