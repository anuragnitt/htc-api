#!/usr/bin/python3
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os.path import dirname, realpath, join
from subprocess import Popen, PIPE
from datetime import datetime
from pytz import timezone as make_tz
from werkzeug.exceptions import HTTPException
import click, json, os, sys, traceback
from typing import List, Tuple


def log_this_event(info: str, tb_msg: str, tz: str, log_file: str)-> None:
    tz = make_tz(tz)
    curr_time = datetime.now(tz)
    curr_time = curr_time.strftime(
        f"[+] %Y-%m-%d %H:%M:%S [TZ: {tz}]"
    )

    log_msg = f"{curr_time}\n\
-------------------------------------------------------\n\
{info}\nEXCEPTION:\n{tb_msg}\
=======================================================\n\n"

    open(log_file, "a").write(log_msg)


def set_executable_mode(bin_file: str)-> None:
    mode = os.stat(bin_file).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(bin_file, mode)


def exec_bin(bin_file: str, args: List[str])-> str:
    set_executable_mode(bin_file)
    argstring = "\n".join(args).encode("utf-8")

    proc = Popen(
        bin_file,
        stdin=PIPE,
        stdout=PIPE
    )
    output, _ = proc.communicate(argstring)

    return output.decode("utf-8")


htc_app = Flask("HTC-API")

limiter = Limiter(
    app=htc_app,
    key_func=lambda: request.headers.get(
        "X-Forwarded-For",
        "127.0.0.1"
    ),
    default_limits=["20/minute"]
)


@htc_app.errorhandler(404)
def invalid_route_handler(e)-> Tuple[str, int]:
    code = e.get_response().status_code
    return f"The route {request.path} doesn't exist", code


@htc_app.errorhandler(429)
def ratelimit_handler(e)-> Tuple[str, int]:
    code = e.get_response().status_code
    max_rate = htc_app.config["max_rate"]
    return f"Maximum allowed execution rate is {max_rate}", code


@htc_app.errorhandler(HTTPException)
def http_exception_handler(e)-> Tuple[str, int]:
    tz = htc_app.config["timezone"]
    log_file = htc_app.config["log_file"]

    info = "This exception was caught in the HTTPException handler"
    tb_msg = traceback.format_exc()
    log_this_event(info, tb_msg, tz, log_file)

    code = e.get_response().status_code
    return f"Oops! A {code} HTTP error occured", code 


@htc_app.errorhandler(Exception)
def server_error_handler(e)-> Tuple[str, int]:
    tz = htc_app.config["timezone"]
    log_file = htc_app.config["log_file"]

    info = "This exception was caught in the general Exception handler"
    tb_msg = traceback.format_exc()
    log_this_event(info, tb_msg, tz, log_file)

    return "A server side error has occured", 500


@htc_app.route("/uptime", methods=["GET"])
@limiter.exempt
def uptime_check()-> Tuple[str, int]:
    return "Don't dig around too much XD", 200


@htc_app.route("/", methods=["GET"])
@limiter.limit(
    limit_value=lambda: limiter.app.config.get(
        "max_rate",
        "20/minute"
    ),
    override_defaults=True
)
def api_handler()-> Tuple[str, int]:

    try:
        if request.method == "GET":

            config_file = htc_app.config["config_file"]
            config = json.load(open(config_file, "r"))
            execmap = config["execmap"]

            params = request.get_json()
            bin_file = join(
                htc_app.config["bin_dir"],
                execmap[params["question"]]
            )

            output = exec_bin(
                bin_file,
                params["args"]
            )

            return output, 200

        else:
            return f"{request.method} method is not implemented", 501

    except Exception as e:
        tz = htc_app.config["timezone"]
        log_file = htc_app.config["log_file"]

        info = f"This event was caught in the execution route handler.\n\
        REQUEST PARAMETERS:\n\
        {json.dumps(params, indent=4)}"
        tb_msg = traceback.format_exc()
        log_this_event(info, tb_msg, tz, log_file)

        return "Invalid parameters", 422


@click.command()
@click.option(
    "--bin-dir",
    help="absolute path to the directory containing the executable files"
)
@click.option(
    "--config",
    help="absolute path to the configuration file"
)
@click.option(
    "--log-file",
    help="absolute path to the error log file"
)
@click.option(
    "--timezone",
    default="Asia/Kolkata",
    help="timezone to use in log timestamps"
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="hostname/IP on which the application is served"
)
@click.option(
    "--port",
    default=8000,
    help="port number on which the application is served"
)
@click.option(
    "--max-rate",
    default="20/minute",
    help="maximum requests allowed per IP address"
)
def main(bin_dir: str, config: str, log_file: str, timezone: str, host: str, port: str or int, max_rate: str)-> None:
    try:
        global htc_app

        htc_app.config.update(
            bin_dir=bin_dir,
            config_file=config,
            log_file=log_file,
            timezone=timezone,
            max_rate=max_rate
        )

        htc_app.run(
            host=host,
            port=port,
            use_reloader=True
        )
    
    except Exception:
        info = "This exception was caught in main()"
        tb_msg = traceback.format_exc()
        log_this_event(info, tb_msg, timezone, log_file)

        return


if __name__ == "__main__":
    main()
