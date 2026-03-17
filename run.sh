
#for file in "data/*/audio/*.mp3";
for file in data/St_Peters_Feb_11_2026_asr/audio/*.mp3;
do
    video=`echo "$file" | cut -d"/" -f2` 
    echo $video

    #for model in "60:5000"; # qwen3-asr
    for model in "69:5008"; # whisper
    do
	echo $model

	echo "offline"
	for segmenter in SHAS SILERO SEAD;
	do
	    echo $segmenter

	    outputfile="hypos/$video-$model-offline-$segmenter.txt"
	    if [ ! -f "$outputfile" ]; then
	    	python ../../2025/audioclient/client.py --asr-kv language=en+it --asr-kv mode=SendUnstable --run-mt en --mt-kv mode=SendPartialAndUnstable -i ffmpeg -f "$file" --no-log --no-textsegmenter --run-tts en --output-file "$outputfile" --print 2 --ffmpeg-speed -1 --asr-kv version=offline --mt-kv version=offline --tts-kv version=offline --asr-kv segmenter=$segmenter
	    fi
	done

	echo "online"
	for segmenter in SILERO SEAD;
	do
	    echo $segmenter

	    outputfile="hypos/$video-$model-online-$segmenter.txt"
	    if [ ! -f "$outputfile" ]; then
	    	python ../../2025/audioclient/client.py --asr-kv language=en+it --asr-kv mode=SendUnstable --run-mt en --mt-kv mode=SendPartialAndUnstable -i ffmpeg -f "$file" --no-log --no-textsegmenter --run-tts en --output-file "$outputfile" --print 2 --send-opus --asr-kv segmenter=$segmenter
	    fi
	    
	done
    done
done

