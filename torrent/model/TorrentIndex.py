from enum import Enum
import json
import os

def enum_converter(obj):
    if isinstance(obj, Enum):
        return obj.value
    else:
        return obj.__dict__
    raise TypeError(f"Tipo {type(obj)} não é serializável!")

class TorrentStatus(Enum):
    COMPLETED = 0
    DOWNLOADING = 1
    QUEUED = 2

class TorrentIndex:
    def __init__(self, json_file, max_download):
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                data = json.load(file)
        else:
            data = {}
        data_clean = {}
        for key, value in data.items():
            data_clean[key] = IndexFile.from_json(value)
        self.files = data_clean
        self.json_file = json_file
        self.max_download = max_download

    def to_json_dict(self):
        return self.__dict__

    def save_file(self):
        with open(self.json_file, "w") as f:
            json.dump(self.files, f, indent=4, default=enum_converter)
    
    def get_number_of_downloading(self):
        count = 0
        for key, value in self.files.items():
            if value.status == TorrentStatus.DOWNLOADING:
                count += 1
        return count

    def get_all_downloading(self):
        torrents = {}
        for key, value in self.files.items():
            if value.status == TorrentStatus.DOWNLOADING:
                torrents[key] = value
        return torrents

    def get_queued(self):
        torrents = {}
        count = 0
        for key, value in self.files.items():
            if value.status == TorrentStatus.QUEUED:
                torrents[key] = value
                count += 1
            if count == self.max_download:
                return torrents
        return torrents


class IndexFile:
    def __init__(self, url, size, status=TorrentStatus.QUEUED):
        self.url = url
        self.size = size
        self.status = status

    def to_json_dict(self):
        return self.__dict__

    @classmethod
    def from_json(cls, data):
        # Converte o status numérico para Enum
        return cls(
            url=data["url"],
            size=data["size"],
            status=TorrentStatus(data["status"]),
        )

