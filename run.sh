# Create folder ./data if not exist
mkdir -p data
# Create folder ./data/audio if not exist
mkdir -p data/audio
sudo docker run -d --restart always -v $(pwd)/data:/app/data -t stream_recorder