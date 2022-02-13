#!/usr/local/bin/python3
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os.path import dirname, realpath, join
from subprocess import Popen, PIPE
from datetime import datetime
from pytz import timezone
import json, os, sys, traceback


cwd = dirname(realpath(__file__))
config_file = join(cwd, "config.json")
log_file = join(cwd, "error.log")
IST = timezone("Asia/Kolkata")


def log_exc(input_params, exc_msg):
    curr_time = datetime.now(IST)
    curr_time = curr_time.strftime("[+] [%Y-%m-%d] [%H:%M:%S] IST")

    log_msg = f"{curr_time}\n--------------------------------------------\n"
    log_msg += f"REQUEST PARAMETERS:\n{input_params}\nEXCEPTION:\n{exc_msg}"
    log_msg += "=======================================================\n\n"
    
    open(log_file, "a").write(log_msg)


def set_executable(binary: str):
    mode = os.stat(binary).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(binary, mode)

def exec_bin(binary: str, args: list)-> str:
    binary = join(cwd, binary)
    set_executable(binary)
    argstring = "\n".join(args).encode("utf-8")

    proc = Popen(binary, stdin=PIPE, stdout=PIPE)
    output, _ = proc.communicate(argstring)

    return output.decode("utf-8")


app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)


@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have exceeded your rate-limit"


@app.route("/", methods=["GET"])
@limiter.limit("300/minute")
def api_handler()-> [str, int]:

    try:
        if request.method == "GET":

            config = json.load(open(config_file, "r"))
            exec_map = config["execMap"]

            params = request.get_json()

            output = exec_bin(
                exec_map[params["question"]],
                params["args"]
            )

            return output, 200

        else:
            return "method not implemented", 501

    except Exception as e:
        input_params = json.dumps(params, indent=4)
        exc_msg = traceback.format_exc()
        log_exc(input_params, exc_msg)

        return "invalid parameters", 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port="3000"
    )

