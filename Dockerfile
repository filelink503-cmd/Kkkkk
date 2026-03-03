# Don't Remove Credit @BabuBhaiKundan
# Subscribe YouTube Channel For Amazing Bot @BabuBhaiKundan
# Ask Doubt on telegram @kundan_yadav_bot

FROM python:3.10.8-slim-bullseye

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /FileToLink
WORKDIR /FileToLink
COPY . /FileToLink
CMD ["python", "bot.py"]
