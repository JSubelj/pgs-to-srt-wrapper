import ffmpeg
import discovery
import conversion

# for f in discovery.discover_mkv("/media"):
#     print("getting subtitles for "+f)
#     conversion.get_eng_subtitles(f)
#     print("fag")
#     print(conversion._extract_and_to_srt_subtitles(f,conversion._get_stream_number(f)))
print("Starting watching for new qbittorrent file",flush=True)
# discovery.watcher("/media",conversion.get_eng_subtitles)
discovery.watch_for_qbittorrent_notifications(conversion.get_eng_subtitles)

# probe=ffmpeg.probe("Supernatural.S01E01.Pilot.1080p.BluRay.REMUX.VC-1.DD.5.1-EPSiLON.mkv")
# print(list(s for s in probe["streams"] if s["codec_name"] == "hdmv_pgs_subtitle" and s["tags"]["language"] == "eng"))