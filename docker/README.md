## Docker image for Callstranger

### Build the image
Before using it, you need to build the image.
To do so, cd into this directory and then run:
```
sudo docker build -t docker-callstranger:latest .
```

### Run the container
To run the container, execute:
```
sudo docker run --net host --rm -ti docker-callstranger:latest
```
Note, you need to run this with `--net host` otherwise the UPnP packages get lost in NAT. 
