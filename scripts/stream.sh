ffmpeg \
-f x11grab \
-s 1600x900 \
-framerate 30 \
-i :20 \
-f lavfi -i anullsrc \
-c:v libx264 \
-b:v 3000k \
-acodec libmp3lame -ar 44100 -b:a 128k \
-preset medium \
-pix_fmt yuv420p \
-r 30 \
-g 10 \
-s 1280x720 \
-threads 0 \
-f tee -map 0:v -map 1:a \
"[f=flv]rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY_1}|[f=flv]rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY_2}"
