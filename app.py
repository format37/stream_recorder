import subprocess
import shlex
import time
import os
import logging

# Define the logging configuration as info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def record_stream(segment_duration=600):  # segment_duration is in seconds (10 minutes)
    logger.info("Recording started.")
    # Define the command to get the stream URL
    streamlink_cmd = "streamlink https://www.1tv.ru/live best -O"
    
    # Start the Streamlink process
    streamlink_process = subprocess.Popen(shlex.split(streamlink_cmd), stdout=subprocess.PIPE)

    # Create data/audio/{project} directory if it doesn't exist
    project = os.environ.get('PROJECT')
    os.makedirs(f"data/audio/{project}", exist_ok=True)1

    # Start recording and segmenting the stream
    while True:
        # Get the current Unix timestamp
        timestamp = int(time.time())
        # Define the FFmpeg command to extract audio, segment it, and save with Unix timestamp
        project = os.environ.get('PROJECT')
        file_path = f"data/audio/{project}/{timestamp}.mp3"
        logger.info(f"Recording to {file_path}")
        ffmpeg_cmd = (
            f"ffmpeg -i pipe:0 -f segment -segment_time {segment_duration} "
            f"-vn -ar 44100 -ac 2 -b:a 192k '{file_path}'"
        )

        # Start the FFmpeg process
        ffmpeg_process = subprocess.Popen(shlex.split(ffmpeg_cmd), stdin=streamlink_process.stdout)
        
        try:
            # Wait for the duration of the segment before starting a new one
            time.sleep(segment_duration)
        except KeyboardInterrupt:
            # Handle the interrupt signal to gracefully shutdown the processes
            streamlink_process.terminate()
            ffmpeg_process.terminate()
            break
    
    print("Recording stopped.")

# Run the recording function
if __name__ == "__main__":
    record_stream()
