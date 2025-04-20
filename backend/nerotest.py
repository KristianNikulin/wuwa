
import ffmpeg

input_path = "2025-04-08 14-00-03.mp4"
output_path = "reversed_video.mp4"

# Команда для разворота видео и аудио
ffmpeg.input(input_path).output(
    output_path,
    vf='reverse',
    af='areverse',
    vcodec='libx264',
    acodec='aac',
    strict='experimental'
).run()