#!/usr/bin/python3
import requests
import sys


"""
interactive consoles wait for an empty line to stop reading
non-interactive consoles (Google Colab) wait for EOFError to occur
"""
def console_input(is_interactive)-> [str]:
    lines = []
    lines_read = 0

    try:
        while True:
            line = input()
            if is_interactive:
                if (len(line) == 0) and (lines_read == 0):
                    continue
                elif len(line) == 0:
                    break
                lines_read += 1
            lines.append(line)
    except EOFError:
        pass

    return lines


def exec_remote(apiUrl, is_interactive=True)-> str:
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
981\n"

    question = sys.argv[1]
    args = []

    if len(sys.argv) > 2:
        args.append(' '.join(sys.argv[2:]))

    args += console_input(is_interactive)

    req_body = {
        "question": question,
        "args": args
    }

    r = requests.get(apiUrl, json=req_body)
    return r.text


def main():
    apiUrl = "https://htc.example.com"
    response = exec_remote(apiUrl, False) # to be used in Google Colab
    print(response)


if __name__ == "__main__":
    main()
