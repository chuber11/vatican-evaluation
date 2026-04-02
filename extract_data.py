
import csv
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

def load_hypos_translated(f):
    data = {"asr":[],"mt":[]}
    with open(f, encoding="utf-8") as fh:
        lines = fh.readlines()

    # Header line: strip trailing semicolons
    headers = list(csv.reader([lines[0].strip().rstrip(";")]))[0]

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Each data line is the full CSV row wrapped in outer double-quotes with trailing ;;
        line = line.rstrip(";")
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1].replace('""', '"')

        try:
            row_fields = list(csv.reader([line]))[0]
        except Exception:
            continue

        if len(row_fields) < 6:
            continue

        row = dict(zip(headers, row_fields))
        start = float(row["start_time"])
        end = float(row["end_time"])
        t = row["timestamp"]

        data["asr"].append({
            "time": t,
            "sender": "asr",
            "start": start,
            "end": end,
            "seq": row["original_text"],
        })
        data["mt"].append({
            "time": t,
            "sender": "mt",
            "start": start,
            "end": end,
            "seq": row["translated_text"],
        })

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
        if f.endswith(".txt"):
            data = load_hypos_kit(f)
        else:
            data = load_hypos_translated(f)

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
