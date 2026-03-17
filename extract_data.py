
import json
import re

def load_hypos_kit(f):
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

def remove_double_spaces(text):
    while True:
        text2 = text.replace("  "," ")
        if len(text2) == len(text):
            break
        text = text2
    return text

def hypos_to_text(f=None, data=None, lowercase=True, remove_punctuation=True):
    if data is None:
        data = load_hypos_kit(f)

    hypo = ""
    for d in data["asr"]:
        if "♪" in d["seq"]:
            continue
        hypo += d["seq"]

    if lowercase:
        hypo = hypo.lower()
    if remove_punctuation:
        hypo = re.sub(r"[^\w\s']", '', hypo)
    hypo = remove_double_spaces(hypo).strip()

    return hypo

def load_references(f):
    data = []
    for line in open(f):
        _, start, end, text = line.strip().split("\t")
        data.append({"start":float(start), "end":float(end), "text":text})
    return data

def references_to_text(f=None, data=None, filter_music=True, filter_choir=True, lowercase=True, remove_punctuation=True):
    if data is None:
        data = load_references(f)

    ref = ""
    for d in data:
        text = d["text"]
        if filter_music:
            text = re.sub(r"<\*\*\*music\*\*\*>.*?</\*\*\*music\*\*\*>", " ", text).strip()
        if filter_choir:
            text = re.sub(r"<\*\*\*choir\*\*\*>.*?</\*\*\*choir\*\*\*>", " ", text).strip()
        ref += text+" "
    
    if lowercase:
        ref = ref.lower()
    if remove_punctuation:
        ref = re.sub(r"[^\w\s']", '', ref)
    ref = remove_double_spaces(ref).strip()

    return ref

if __name__ == "__main__":
    id = "St_Peters_Feb_11_2026_asr"

    hypos_text = hypos_to_text(f"hypos/{id}-69:5008-offline-SHAS.txt")
    print(hypos_text)

    references_text = references_to_text(f"data/{id}/transcription.txt")
    print(references_text)
