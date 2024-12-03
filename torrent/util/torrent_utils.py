import json
import logging
import os
import asyncio
from torrentp import TorrentDownloader
from functools import partial

from model.TorrentIndex import IndexFile, TorrentIndex, TorrentStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def callback(task, key, torrent_index):
    torrent_index.files[key].status = TorrentStatus.COMPLETED
    # report a message
    print('Task is done')
    print(key)

def update_torrents_list(torrent_index):
    root_dir = os.getenv('TORRENT_PATH')
    file_list: list[dict] = []
    for directory, _, files in os.walk(root_dir):
        for file_name in files:
            if file_name.lower().endswith(('.torrent')):
                rel_dir = os.path.relpath(directory, root_dir)
                if rel_dir != '.':
                    rel_file = os.path.join(rel_dir, file_name)
                else:
                    rel_file = file_name
                if file_name not in torrent_index.files:
                    torrent_index.files[file_name] = IndexFile(rel_file, os.path.getsize(os.path.join(root_dir, rel_file)))
                # file_list.append(IndexFile('../' + rel_file,
                #                            os.path.getsize(os.path.join(root_dir, rel_file))).to_json_dict())
                # logger.info(os.path.join(root_dir, rel_file))

async def download_torrents(torrent_index, torrents):
    root_dir = os.getenv('TORRENT_PATH')
    tasks = []
    for key, value in torrents.items():
        torrent_index.files[key].status = TorrentStatus.DOWNLOADING
        torrent_file = TorrentDownloader(os.path.join(root_dir, value.url), os.getenv('GAMES_PATH'))
        task = asyncio.create_task(torrent_file.start_download())
        task.add_done_callback(partial(callback, key=key, torrent_index=torrent_index))
        tasks.append(task)
    if len(tasks) > 0:
        _ = await asyncio.wait(tasks)

def write_shop_index() -> None:
    torrent_index = TorrentIndex(os.getenv('TORRENT_PATH')+'/'+os.getenv('TORRENT_JSON_FILE'), int(os.getenv('MAX_DOWNLOAD')))
    update_torrents_list(torrent_index)
    if torrent_index.get_number_of_downloading() > 0:
        #Start the download from theses
        torrents = torrent_index.get_all_downloading()
    else:
        #Start the download from queued and to max
        torrents = torrent_index.get_queued()
    print(torrents)
    asyncio.run(download_torrents(torrent_index, torrents))
    torrent_index.save_file()
    # shop_index.files = create_games_list()
    # asyncio.run(download_torrents(torrents))
    # shop_files = ['shop.json', 'shop.tfl']
    # for shop in shop_files:
    #     try:
    #         with open(os.getenv('SHOP_PATH') + '/' + shop, 'w') as file:
    #             file.write(json.dumps(shop_index.to_json_dict(), indent=4))
    #             logger.info(f'{shop} created successfully')
    #     except Exception as e:
    #         logger.error(f'Error creating {shop}:\n{e}')


