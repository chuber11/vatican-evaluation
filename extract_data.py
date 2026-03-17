
import json
from glob import glob

def extract_data_kit(f):
    data = {"asr":[],"mt":[]}
    for line in open(f):
        t, content = line.strip().split("▁")
        t, content = float(t), json.loads(content)

        if "unstable" in content and content["unstable"]:
            continue
        if "controll" in content:
            continue

        message = {"time":t}

        sender = content["sender"].split(":")[0]
        message["sender"] = sender
        if "signal" in content:
            continue
        elif sender in ["asr","mt"]:
            message["start"] = float(content["start"])
            message["end"] = float(content["end"])
            message["seq"] = content["seq"]
        else:
            #message["text"] = content["text"]
            continue

        data[sender].append(message)
    return data

if __name__ == "__main__":
    for f in glob("hypos/*"):
        print(f)
        data = extract_data_kit(f)
        print(data)
        break

