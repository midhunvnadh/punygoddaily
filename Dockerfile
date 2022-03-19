FROM ubuntu:20.04
ENV DEBIAN_FRONTEND "noninteractive"
WORKDIR /bot
ADD . /bot

RUN echo "" > files/*.txt

RUN apt-get update && \
    apt install -y python3.8 python3.8-dev python3-pip ffmpeg && \
    pip install instagrapi bs4 requests Pillow moviepy

CMD ["python3", "-u", "start.py"]