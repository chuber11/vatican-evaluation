
Folder structure:

data/$id/transcription.txt
data/$id/audio/ -> mp3 file

Run KIT Lecture translator:

bash run.sh

Hypotheses are saved in hypos/*.txt

Calculate WER:

python evaluate.py

