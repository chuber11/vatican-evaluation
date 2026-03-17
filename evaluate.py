
from jiwer import wer, process_words, visualize_alignment
from extract_data import hypos_to_text, references_to_text

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
    id = "St_Peters_Feb_11_2026_asr"

    model_to_server = {"whisper": "69:5008", "qwen3-asr": "60:5000"}

    for version in ["offline","online"]:
        #for model in ["whisper","qwen3-asr"]:
        for model in ["whisper"]:
            for segmenter in ["SHAS","SEAD","SILERO"]:
                try:
                    hypos_text = hypos_to_text(f"hypos/{id}-{model_to_server[model]}-{version}-{segmenter}.txt")
                except:
                    continue
                references_text = references_to_text(f"data/{id}/transcription.txt")

                wer_ = calc_wer(hypos_text, references_text, verbose=False)
                print(f"Model: {model:9s}, version: {version:7s}, segmenter: {segmenter:6s}, WER: {wer_:5.2f}%")

