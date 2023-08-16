from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm
import os
import requests
import string
import openpyxl
import rich
from rich import print as cetak
from rich.panel import Panel as nel

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

os.system("chmod 777 video")
cetak(nel('[red]Masukan Link Video dari Tiktok',width=70,padding=(0,7)))
linkvidtt = input('>>> ')
with open('link.txt', "a") as peler:
 peler.write(linkvidtt)

# Open the file and count the lines
try:
  with open('link.txt', "r") as linkvid:
    lines = linkvid.readlines()  # Read all lines into a list

    for i, line in enumerate(lines, start=2):  # Start from row 2
        linkvideo = f"{line.strip()}"
        cetak(nel('[yellow]Getting info...',width=70,padding=(0,7)))
        print('Link Video : ',linkvideo)
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
        }

        params = {
            'url': linkvideo,
            'update': '1',
        }

        response = session.get(
            'https://dl1.tikmate.cc/listFormats', params=params, headers=headers).json()
        video = response['formats']['video'][0]['url']
        tittlesr = response['formats']['title']
        creator = response['formats']['creator']
        tittles = tittlesr.replace(" ", "_")  # Replace spaces with underscores
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        tittle = ''.join(c for c in tittles if c in valid_chars)
        print(creator)
        print(tittlesr)

        if not os.path.exists('video'):
            os.makedirs('video')

        # Download the video and show a progress bar
        video_filename = f"video/{tittle}.mp4"
        response = requests.get(video, stream=True)

        # Get the total size of the file from the content-length header
        total_size = int(response.headers.get('content-length', 0))

        # Use the 'with' statement for both file and tqdm
        with open(video_filename, 'wb') as file, tqdm(
                desc=f"Downloading",
                total=total_size,
                unit='B', unit_scale=True, unit_divisor=1024,
                ascii=True
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                bar.update(len(data))

        cetak(nel('[green]Download selesai!',width=70,padding=(0,7)))


  os.system("rm link.txt")
  os.system("cp -r video /sdcard")
  print(f'Video saved in /storage/emulated/0/video')
except KeyError:
  print("Masukan Url yang benar!")
  os.system("rm link.txt")
except KeyboardInterrupt:
  print("Program dihentikan!")
