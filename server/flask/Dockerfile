FROM python

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /opt/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /opt/app/front-end/src

ENTRYPOINT [ "python", "app.py" ]
