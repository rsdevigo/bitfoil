FROM python:3.10.9-alpine

RUN mkdir /torrent
COPY . /torrent
RUN pip install --no-cache-dir -r /torrent/requirements.txt

CMD [ "python", "/torrent/main.py" ]
