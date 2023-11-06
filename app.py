import subprocess
import shlex
import time

def record_stream(segment_duration=600):  # segment_duration is in seconds (10 minutes)
    # Define the command to get the stream URL
    streamlink_cmd = "streamlink https://www.1tv.ru/live best -O"
    
    # Define the FFmpeg command to extract audio and split it into segments
    # ffmpeg_cmd = ("ffmpeg -i pipe:0 -f segment -segment_time {duration} "
    #               "-c copy -vn -strftime 1 'output_%Y-%m-%d_%H-%M-%S.mp3'").format(duration=segment_duration)
    ffmpeg_cmd = ("ffmpeg -i pipe:0 -f segment -segment_time {duration} "
              "-vn -ar 44100 -ac 2 -b:a 192k -strftime 1 'data/audio/output_%Y-%m-%d_%H-%M-%S.mp3'").format(duration=segment_duration)

    
    # Start the Streamlink process
    streamlink_process = subprocess.Popen(shlex.split(streamlink_cmd), stdout=subprocess.PIPE)
    
    # Start the FFmpeg process
    ffmpeg_process = subprocess.Popen(shlex.split(ffmpeg_cmd), stdin=streamlink_process.stdout)
    
    try:
        # Wait for the FFmpeg process to finish (it won't if it's a 24/7 stream)
        ffmpeg_process.wait()
    except KeyboardInterrupt:
        # Handle the interrupt signal to gracefully shutdown the processes
        streamlink_process.terminate()
        ffmpeg_process.terminate()
        
    print("Recording stopped.")

# Run the recording function
if __name__ == "__main__":
    record_stream()
