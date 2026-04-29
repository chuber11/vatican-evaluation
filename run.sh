
#for file in "data/*/audio/*.mp3";
for file in data/St_Peters_Feb_11_2026_asr/audio/*.mp3;
do
    video=`echo "$file" | cut -d"/" -f2` 
    echo $video

    model="60:5008"
    echo $model

    echo "online"
    for segmenter in SILERO; # SILERO_TUNED;
    do
	echo $segmenter

	for n in {0..4}
	do
	    outputfile="hypos/$video-$model-online-$segmenter-$n.txt"
	    if [ ! -f "$outputfile" ]; then
		python ../../2025/audioclient/client.py --asr-kv language=en+it --asr-kv mode=SendUnstable --run-mt en --mt-kv mode=SendPartialAndUnstable -i ffmpeg -f "$file" --no-log --no-textsegmenter --run-tts en --output-file "$outputfile" --print 2 --send-opus --asr-kv segmenter=$segmenter
	    fi
	done
    done
done

