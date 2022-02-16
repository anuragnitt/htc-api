#!/usr/bin/python3
import requests
import sys


def exec_remote(apiUrl, vidUrl)-> str:
    if any((
        len(sys.argv) < 2,
        sys.argv[1] == "--help",
        sys.argv[1] == "-h"
    )):
        return f"Instructions to use:\n\
{sys.argv[0]} <question>\n\
<first input line>\n\
...\n\
<last input line>\n\n\
Example:\n\
{sys.argv[0]} q1\n\
981\n\n\
Tutorial video: {vidUrl}\n"

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
    vidUrl = open("video-tutorial.url").read().strip()

    response = exec_remote(apiUrl, vidUrl)
    print(response)


if __name__ == "__main__":
    main()

