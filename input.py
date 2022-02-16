#!/usr/bin/python3
import requests
import sys


def exec_remote(apiUrl)-> str:
    if len(sys.argv) < 2:
        print("mention question number")
        return

    question = sys.argv[1]
    args = []

    if len(sys.argv) > 2:
        args.append(' '.join(sys.argv[2:]))

    while True:
        line = input()
        if not line:
            break
        else:
            args.append(line)

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

