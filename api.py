#!/usr/bin/python3
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os.path import dirname, realpath, join
from subprocess import Popen, PIPE
from datetime import datetime
from pytz import timezone as make_tz
from werkzeug.middleware.proxy_fix import ProxyFix
import click, json, os, sys, traceback


def get_log_msg(input_params, tb_msg, tz):
    tz = make_tz(tz)
    curr_time = datetime.now(tz)
    curr_time = curr_time.strftime(f"[+] %Y-%m-%d %H:%M:%S [TZ: {tz}]")

    log_msg = f"{curr_time}\n--------------------------------------------\n"
    log_msg += f"REQUEST PARAMETERS:\n{input_params}\nEXCEPTION:\n{tb_msg}"
    log_msg += "=======================================================\n\n"
    
    return log_msg


def set_executable_mode(bin_file: str):
    mode = os.stat(bin_file).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(bin_file, mode)


def exec_bin(bin_file: str, args: list)-> str:
    set_executable_mode(bin_file)
    argstring = "\n".join(args).encode("utf-8")

    proc = Popen(bin_file, stdin=PIPE, stdout=PIPE)
    output, _ = proc.communicate(argstring)

    return output.decode("utf-8")


app = Flask("HTC-API")


@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have reached the maximum allowed request rate", 429


@app.route("/", methods=["GET"])
def api_handler()-> [str, int]:

    try:
        if request.method == "GET":

            config_file = app.config["config_file"]
            config = json.load(open(config_file, "r"))
            execmap = config["execmap"]

            params = request.get_json()
            bin_file = join(app.config["bin_dir"], execmap[params["question"]])

            output = exec_bin(bin_file, params["args"])

            return output, 200

        else:
            return "method not implemented", 501

    except Exception as e:
        log_file = app.config["log_file"]
        tz = app.config["timezone"]

        input_params = json.dumps(params, indent=4)
        tb_msg = traceback.format_exc()
        log_msg = get_log_msg(input_params, tb_msg, tz)

        open(log_file, "a").write(log_msg)

        return "invalid parameters", 400


@click.command()
@click.option("--bin-dir", help="absolute path to the directory containing the executable files")
@click.option("--config", help="absolute path to the configuration file")
@click.option("--log-file", help="absolute path to the error log file")
@click.option("--timezone", default="Asia/Kolkata", help="timezone to use in log timestamps")
@click.option("--port", default=8000, help="port number to run the application on")
@click.option("--max-rate", default=15, help="maximum requests allowed per minute per user")
def main(bin_dir, config, log_file, timezone, port, max_rate):

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=True)

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{max_rate}/minute"]
    )
    limiter.init_app(app)

    app.config.update(
        bin_dir=bin_dir,
        config_file=config,
        log_file=log_file,
        timezone=timezone
    )

    app.run(
        host="0.0.0.0",
        port=port,
        use_reloader=True
    )


if __name__ == "__main__":
    main()

