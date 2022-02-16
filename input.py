#!/usr/bin/python3
import requests
import sys


howtorun = f"Instructions to use:\n\
{sys.argv[0]} <question>\n\
<first input line>\n\
...\n\
<last input line>\n\n\
Example:\n\
{sys.argv[0]} q1\n\
981\n"


def exec_remote(apiUrl)-> str:
    if any((
        len(sys.argv) < 2,
        sys.argv[1] == "--help",
        sys.argv[1] == "-h"
    )):
        return howtorun

    question = sys.argv[1]
    args = []

    if len(sys.argv) > 2:
        args.append(' '.join(sys.argv[2:]))

    try:
        while True:
            args.append(input())
    except EOFError:
        pass

    req_body = {
        "question": question,
        "args": args
    }

    r = requests.get(apiUrl, json=req_body)
    return r.text


def main():
    apiUrl = "https://urtc.example.com"
    response = exec_remote(apiUrl)
    print(response)


if __name__ == "__main__":
    main()

