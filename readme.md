# Vietnamese speech recognition web demo

## Pull docker image
```
    docker pull wav2letter/wav2letter:inference-latest
```
## For using GPUs
---
### Install nvidia-docker for utilizing nvidia GPUs
```
    https://github.com/NVIDIA/nvidia-docker
```
### Create docker container
```
    docker run -p 5001:5001 --gpus all -itd --ipc=host --volume /full/path/to
/vietnamese-wave2letter-stream-convnet-web-demo:/root/src --name w2l wav2letter/wav2letter:inference-latest
```
## For using CPU
### Create docker container
```
    docker run -p 5001:5001 -itd --ipc=host --volume /full/path/to
/vietnamese-wave2letter-stream-convnet-web-demo:/root/src --name w2l wav2letter/wav2letter:inference-latest
```
## After that do these things
### Put model into ./model
Change db host ip ./statis/js/config.js
### Run
```
    docker exec -it w2l bash
    cd /root/src/
    export PYTHONIOENCODING=utf8
    python3 app.py
```

## Test with file only
```
    python3 service.py
```
**Go to browser**
```
    ex: ....:5001?filepath=/path/to/audio/file.
```
