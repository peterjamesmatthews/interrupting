import time

from flask import Flask
from timeout import exceptional_timeout, timeout

app = Flask(__name__)


@app.route("/v1/sleep/<string:num>/echo/<string:msg>")
def sleep_echo_1(num: str, msg: str):
    time.sleep(float(num))
    return msg


@app.route("/v2/sleep/<string:num>/echo/<string:msg>")
@timeout(1)
def sleep_echo_2(num: str, msg: str):
    time.sleep(float(num))
    app.logger.debug("Slept")
    return msg


@app.route("/v3/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_3(num: str, msg: str):
    start = time.time()
    n = float(num)
    while time.time() - start < n:
        app.logger.debug("Sleeping")
        time.sleep(0.1)
    return msg


@app.route("/v4/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_4(num: str, msg: str):
    start = time.time()
    n = float(num)
    while time.time() - start < n:
        app.logger.debug("Spinning")
    return msg


lock = False


def get_lock():
    global lock
    while lock:
        time.sleep(0.1)
    lock = True
    return lock


def release_lock():
    global lock
    lock = False
    return lock


@app.route("/v5/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_5(num: str, msg: str):
    get_lock()
    time.sleep(float(num))
    release_lock()
    return msg


@app.route("/v6/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_6(num: str, msg: str):
    try:
        get_lock()
        time.sleep(float(num))
    finally:
        release_lock()
    return msg
