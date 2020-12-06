import ffmpeg
import subprocess
import re
import shlex
import os
from datetime import datetime

DOTNET_EXECUTABLE = os.getenv("DOTNET_EXECUTABLE") if os.getenv("DOTNET_EXECUTABLE") else "./dotnet/dotnet"
PGSTOSRT_DLL = os.getenv("PGSTOSRT_DLL") if os.getenv("PGSTOSRT_DLL") else "./PgsToSrt/PgsToSrt.dll"

def _get_stream_number(path_to_mkv):
    probe=ffmpeg.probe(path_to_mkv)
    # Added one because ffmpeg has 0-start intexes and stream number is really +1
    l = list(s for s in probe["streams"] if s["codec_name"] == "hdmv_pgs_subtitle" and s["tags"]["language"] == "eng")
    return l[0]["index"]+1 if len(l) > 0 else None

# SDH

def _extract_and_to_srt_subtitles(path_to_mkv, stream_no):
    # dotnet /mnt/c/Users/CleptesGameStation/Downloads/PgsToSrt-1.2.0/PgsToSrt.dll --input test/test/Supernatural.S01E01.Pilot.1080p.BluRay.REMUX.VC-1.DD.5.1-EPSiLON.mkv --output ./test.srt --track 4
    f = open(re.sub(r'.mkv$','.pgstosrt.log',path_to_mkv),"w")
    subprocess.run(shlex.split(f"{DOTNET_EXECUTABLE} {PGSTOSRT_DLL} --input \"{path_to_mkv}\" --output \"{re.sub(r'.mkv$','.srt',path_to_mkv)}\" --track {str(stream_no)}"), stdout=f, stderr=subprocess.STDOUT)
    f.close()

def _check_if_already_exists(path_to_mkv):
    return os.path.exists(re.sub(r'.mkv$','.srt',path_to_mkv))

def get_eng_subtitles(path_to_mkv):
    if not _check_if_already_exists(path_to_mkv):
        no = _get_stream_number(path_to_mkv)
        if no is not None:
            print(datetime.now(), "Starting conversion to srt track number:",no,"; file:",path_to_mkv,flush=True)
            _extract_and_to_srt_subtitles(path_to_mkv,no)

if __name__=="__main__":
    import sys
    #print(sys.argv[1])
    get_eng_subtitles(sys.argv[1])
    