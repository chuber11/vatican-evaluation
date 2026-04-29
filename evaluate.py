
from jiwer import wer, process_words, visualize_alignment
from extract_data import hypos_to_text, references_to_text
from glob import glob
from pathlib import Path

"""def calculate_latency(data):
    sum_seconds = 0
    sum_weight = 0
    for segment in data:
        weight = len(segment["seq"]) #segment["end"] - segment["start"]
        t_arrive = segment["time"]
        t_middle = (segment["start"] + segment["end"]) / 2

        #if t_arrive-t_middle > 15:
        #    print(t_arrive-t_middle,weight,segment)
        sum_seconds += weight * (t_arrive-t_middle)
        sum_weight += weight
    return sum_seconds/sum_weight"""

def print_alignment(alignment, l=140):
    alignment = alignment.split("\n")
    print("=== ALIGNMENT ===")
    ref = alignment[2][4:]
    hyp = alignment[3][4:]
    sid = alignment[4][4:]
    while True:
        l_ = l
        while len(ref) > l_ and ref[l_] != " ":
            l_ += 1
        print(f"REF:{ref[:l_]}")
        print(f"HYP:{hyp[:l_]}")
        print(f"    {sid[:l_]}")
        ref = ref[l_:]
        hyp = hyp[l_:]
        sid = sid[l_:]
        if not ref:
            break
    for a in alignment[6:]:
        print(a)

def calc_wer(hypothesis, reference, verbose=False):
    # Compute WER
    wer_ = wer(reference, hypothesis)

    # Get detailed alignment
    output = process_words(reference, hypothesis)

    alignment = visualize_alignment(output)
    if verbose:
        print_alignment(alignment)

    return 100*wer_

if __name__ == "__main__":
    model_to_server = {"whisper": "60:5008", "qwen3-asr": "60:5000"}
    server_to_model = {v: k for k, v in model_to_server.items()}

    verbose = False

    ids = ["St_Peters_Feb_11_2026_asr"]

    for f in sorted(glob("hypos/*.txt")):
        parts = Path(f).stem.split("-")
        # filename pattern: {id}-{server}-{version}-{segmenter}-{num}
        # server contains ':' but no '-', so splitting from the end is safe
        num, segmenter, version, server = parts[-1], parts[-2], parts[-3], parts[-4]
        id = "-".join(parts[:-4])
        model = server_to_model.get(server, server)

        references_text = references_to_text(f"data/{id}/transcription.txt")
        try:
            hypos_text = hypos_to_text(f)
        except Exception:
            continue

        wer_ = calc_wer(hypos_text, references_text, verbose=verbose)
        print(f"Id: {id}, model: {model:9s}, version: {version:7s}, segmenter: {segmenter:6s}, WER: {wer_:5.2f}%")

    for id in ids:
        references_text = references_to_text(f"data/{id}/transcription.txt")
        hypos_text = hypos_to_text(f"hypos/{id}-translated.csv")
        wer_ = calc_wer(hypos_text, references_text, verbose=verbose)
        print(f"Id: {id}, model: translated, WER: {wer_:5.2f}%")

