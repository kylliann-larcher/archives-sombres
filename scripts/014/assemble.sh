set -e
cd /home/claude/work014
ls shots/shot_*.mp4 | sort | sed "s|^|file '/home/claude/work014/|;s|$|'|" > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy video_raw.mp4
ffmpeg -y -loglevel error -i voix2.wav -i tension14.wav -i sfx14.wav -filter_complex "[0:a]volume=1.0[v];[1:a]volume=0.30[m];[2:a]volume=0.55[s];[v][m][s]amix=inputs=3:duration=first:normalize=0[a]" -map "[a]" -ar 44100 mix.wav
ffmpeg -y -loglevel error -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 44100 mix_norm.wav
ffmpeg -y -loglevel error -i video_raw.mp4 -i mix_norm.wav -vf "ass=cap14.ass:fontsdir=/usr/share/fonts/truetype/google-fonts" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest video-014-v2-molay.mp4
ls -la video-014-v2-molay.mp4
