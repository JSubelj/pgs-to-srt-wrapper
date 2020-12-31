# PgsToSrtWrapper

Command and daemon to transform english from PGS mkv file to srt subtitles. This is just wrapper of PgsToSrt from Tentacule: https://github.com/Tentacule/PgsToSrt
Subtitles are created in the same directory as mkv. Log of conversion is also created with file ending in .pgstosrt.log.

I created this software because Plex client on my TV is retarded and can't display PGS subtitles without transcoding.

## Prerequirements (Linux)
- ffmpeg
- tesseract
- Python >=3.8

## Instalation
- Download and extract zip: https://github.com/JSubelj/pgs-to-srt-watcher/archive/master.zip
- Download latest release from PgsToSrt: https://github.com/Tentacule/PgsToSrt
- Extract PgsToSrt to PgsToSrtWrapper/PgsToSrt directory
- Download wanted english traineddata from https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata and place into PgsToSrtWrapper/PgsToSrt/tessdata
- Download dotnet 5 and extract to PgsToSrtWrapper/dotnet from https://dotnet.microsoft.com/download/dotnet/5.0
- Create virtual environment and install requirements in PgsToSrtWrapper directory: `python -m venv venv && . venv/bin/activate && pip install -r requirements.txt`
- Make pgs-to-srt executable: `chmod +x pgs-to-srt`
- You can use update.sh for updating PgsToSrt.

Your file tree should look something like this:
```
.
├── create_file.sh
├── Dockerfile
├── pgs-to-srt
├── PgsToSrt-1.3.0.zip
├── PgsToSrtWrapper
│   ├── conversion.py
│   ├── discovery.py
│   ├── dotnet/
│   ├── main.py
│   ├── PgsToSrt/
│   ├── requirements.txt
│   └── venv/
├── README.md
├── rebuildandrun.sh
└── update.sh
```

## Run (standalone)
To run use: `pgs-to-srt moviefile.mkv`

## Docker
Docker daemon should be used with qbittorrent or any other client that support adding downloaded path string to file after torrent is completed.

You can run docker daemon with compose as such:
```
version: '2'

services:
    pgs-to-srt-watcher:
        image: cleptes/pgs-to-srt-file-watcher     
        container_name: pgs-to-srt-watcher
        restart: always
        volumes:
            - {folder_to_your_media_root}:/downloads
        environment:
            - SLEEPING_TIME_S=1 # Time to sleep between pooling qbittorrent_notification.txt file
            - UID=1000 # User id
            - GID=1000 # Group id
```

QBittorrent downloads folder should also point to {folder_to_your_media_root}.

### QBittorrent setup
- QBittorrent should have access to create_file.sh script.
- In Tools -> Options-> Downloads check 'Run external program on torrent completion' and point it to create_file.sh with %F flag. In my case: `/config/create_file.sh %F` 
- This creates a qbittorrent_notification.txt file on root of your media folder 
- When daemon sees qbittorrent_notification.txt file it reads it and removes it, then starts conversion. 


### MOST IMPORTENDLY
I am not responsible for your seed ratio if my software deletes ur files or any other retarded shit that can happen if my software glitches horribly. This software also does not promote piracy in any way shape or form and is used only to download and convert videos that you own and just so happen you copy it from one computer to another with bittorrents because u never learned what scp or rsync is.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

