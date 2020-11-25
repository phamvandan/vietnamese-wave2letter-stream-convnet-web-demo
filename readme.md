# Vietnamese speech recognition web demo

## Pull docker image
```
    docker pull wav2letter/wav2letter:inference-latest
```
## Install nvidia-docker for utilizing nvidia GPUs
```
    https://github.com/NVIDIA/nvidia-docker
```
## Create docker container
```
    docker run -p 5001:5001 --gpus all -itd --ipc=host --volume /full/path/to
/vietnamese-wave2letter-stream-convnet-web-demo:/root/src --name w2l wav2letter/wav2letter:inference-latest
```
### Put model into ./model
Change db host ip ./statis/js/config.json
### Run
```
    python3 app.py
```