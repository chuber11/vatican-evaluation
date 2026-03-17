
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
    if verbose:
        print(f"WER: {100*wer_:.2f}%")

    # Get detailed alignment
    output = process_words(reference, hypothesis)

    alignment = visualize_alignment(output)
    if verbose:
        print_alignment(alignment)

    return 100*wer_

if __name__ == "__main__":
    id = "St_Peters_Feb_11_2026_asr"

    hypos_text = hypos_to_text(f"hypos/{id}-69:5008-offline-SHAS.txt")
    references_text = references_to_text(f"data/{id}/transcription.txt")

    wer_ = calc_wer(hypos_text, references_text)
    print(f"WER: {wer_:.2f}%")
