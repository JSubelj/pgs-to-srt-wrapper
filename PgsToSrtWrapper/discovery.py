import glob
import os
import time
import threading
import queue
from datetime import datetime
import multiprocessing

SLEEPING_TIME_S = int(os.getenv("SLEEPING_TIME_S"))

def discover_mkv(path):
    return list(os.path.abspath(f) for f in glob.glob(os.path.join(path,"**/*.mkv"),recursive=True))



def watch_for_qbittorrent_notifications(on_new):
    while True:
        if os.path.exists("/downloads/qbittorrent_notification.txt"):
            print(datetime.now(),"[NewFilesWatcher]","qbittorrent_notification.txt exists",flush=True)
            content = ""
            with open("/downloads/qbittorrent_notification.txt","r") as f:
                print(datetime.now(),"[NewFilesWatcher]","reading qbittorrent_notification.txt",flush=True)
                content = f.read()
            print(datetime.now(),"[NewFilesWatcher]","removing qbittorrent_notification.txt",flush=True)
            os.unlink("/downloads/qbittorrent_notification.txt")

            dirs = content.split("\n")
            for f in dirs:
                f=f.strip()
                if not f:
                    break
                print(datetime.now(),"[NewFilesWatcher]",f"processing file/dir {f}",flush=True)
                if f.endswith(".mkv"):
                    print(datetime.now(),"[NewFilesWatcher]",f"File {f} is mkv doing conversion now",flush=True)

                    multiprocessing.Process(target=start_conversion, args=(f, on_new)).start()
                else:
                    print(datetime.now(),"[NewFilesWatcher]",f"Discovering mkvs in dir {f}",flush=True)

                    files = discover_mkv(f)
                    for ff in files:
                        print(datetime.now(),"[NewFilesWatcher]",f"Starting conversion of {ff}",flush=True)
                        multiprocessing.Process(target=start_conversion, args=(ff, on_new)).start()
        else:
            time.sleep(SLEEPING_TIME_S)


def _watch_for_new_files(path, q, already_done = None):
    if already_done is None:
        already_done = []

    while True:
        files = discover_mkv(path)
        for f in files:
            if f in already_done:
                pass
            else:
                q.put(f)
                print(datetime.now(),"[NewFilesWatcher]","New file discovered:",f,flush=True)
                already_done.append(f)
        time.sleep(SLEEPING_TIME_S)

def _watch_file(path):
    old_size = 0
    new_size = os.path.getsize(path)
    print(datetime.now(),"[FileChangeWatcher]","Watching file:",path,flush=True)
    while new_size != old_size:
        old_size=new_size
        time.sleep(SLEEPING_TIME_S)
        new_size=os.path.getsize(path)
        print("new size:",new_size, "old_size:", old_size)
    print(datetime.now(),"[FileChangeWatcher]",f"File didn't change in {SLEEPING_TIME_S} seconds:",path,flush=True)

def start_conversion(path, exec):
    print(datetime.now(),"[Process.Watcher]","File ready for conversion", path,flush=True)
    exec(path)
    print(datetime.now(),"[Process.Watcher]","Conversion done", path,flush=True)


def watcher(path, on_new):
    threads = []
    q = queue.Queue()

    new_files_watcher = threading.Thread(target=_watch_for_new_files, args=(path,q, discover_mkv(path) if os.getenv("SKIP_DISCOVERY") == "TRUE" else None))
    new_files_watcher.start()
    print(datetime.now(),"[Watcher]","Started file watcher", flush=True)

    while True:
        try:
            new_file = q.get_nowait()
            print(datetime.now(),"[Watcher]","Got new file from watcher: ",new_file,flush=True)
            nt = threading.Thread(target=_watch_file, args=(new_file,))
            nt.start()
            threads.append((new_file, nt))
        except queue.Empty:
            pass
        to_del = []
        for i in range(0,len(threads)):
            if not threads[i][1].is_alive():
                to_del.append(i)
                multiprocessing.Process(target=start_conversion, args=(threads[i][0], on_new)).start()

        for inx in to_del:
            del threads[inx]
        time.sleep(SLEEPING_TIME_S)
    
    



    