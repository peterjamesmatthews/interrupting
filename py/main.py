import time

from flask import Flask
from timeout import exceptional_timeout, timeout

app = Flask(__name__)


@app.route("/v1/sleep/<string:num>/echo/<string:msg>")
def sleep_echo_1(num: str, msg: str):
    """No timeout."""
    time.sleep(float(num))
    return msg


@app.route("/v2/sleep/<string:num>/echo/<string:msg>")
@timeout(1)
def sleep_echo_2(num: str, msg: str):
    """With timeout."""
    time.sleep(float(num))
    app.logger.debug("Slept")  # will still execute after timeout
    return msg


@app.route("/v3/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_3(num: str, msg: str):
    """With exceptional timeout."""
    time.sleep(float(num))
    app.logger.debug("Slept")  # won't execute after timeout
    return msg


lock = False


def get_lock():
    global lock
    while lock:
        pass
    lock = True
    return lock


def release_lock():
    global lock
    lock = False
    return lock


@app.route("/v4/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_4(num: str, msg: str):
    """With exceptional timeout and unsafe lock."""
    get_lock()
    time.sleep(float(num))
    release_lock()  # won't execute after timeout, deadlock!
    return msg


@app.route("/v5/sleep/<string:num>/echo/<string:msg>")
@exceptional_timeout(1)
def sleep_echo_5(num: str, msg: str):
    """With exceptional timeout and safe lock."""
    try:
        get_lock()
        time.sleep(float(num))
    finally:
        release_lock()  # will execute after timeout, no deadlock
    return msg
