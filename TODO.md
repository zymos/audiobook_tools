# Entire package
* create setup/install
  * copy to python dir
  * copy main exe to bin
  * make copy config to .config 
* create other package (deb, ...)

Create seperate online-tts package (maybe)

#web-novel-tts (create)
* joining web-novel-to-text and online-tts
* remove non-latin1 charators option
  * https://stackoverflow.com/questions/23680976/python-removing-non-latin-characters

# web-novel-to-text
* add other web-novel sites
* remove non eu (needs fixed)

# online-tts
* remove_nonstandard_chars seems to be locked up for too much time
* implement profiles
* add amazion polly, ibm, google cloud support
* check timeout-retry (error response) maybe subsplit
* Bug: File does not exist shows as 0 files

# audiobook-reenconder
* Create temp dir per instance ?done?
* Add parallel process files
* test output m4b, ogg, opus
* *add cover art non mp3
* remove all non-audio/image
* Bug
  * chap with ~= 0 should be ignored: Done?
  * -new is moveing wrong thing
  * fix input bandwidth < output bandwidth: skip
  * Seas the Day: Bad Guys Series, Book 5/ Initiate: Animus, Book 1/ no encoded by
  * no delete old
  * split not copying
  * bitrate lower not good with m4b, check valid bitrate, check formate



  p04:43:26:  ~ CMD: ffmpeg -loglevel error -y -i "/tmp/audiobook_reencode/13439492/5/temp-single-48520445580157.mp3" -t 14.54 -c:v copy -c:a copy "/tmp/audiobook_reencode/13439492/5/01 Hive Knight/001.mp3"
04:43:26:  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
04:43:26:          Spliting chapter: 1/32
04:43:26: Error: encoding failed!
ffmpeg command:
>ffmpeg -loglevel error -y -i "/tmp/audiobook_reencode/13439492/5/temp-single-48520445580157.mp3" -t 14.54 -c:v copy -c:a copy "/tmp/audiobook_reencode/13439492/5/01 Hive Knight/001.mp3"
04:43:26: ffmpeg error: b'/tmp/audiobook_reencode/13439492/5/01 Hive Knight/001.mp3: No such file or directory\n'
04:43:26: Exiting after failure
╭─ /pub/books/000TO_REECODE ───────────────

ls /tmp/audiobook_reencode/13439492/5                                            ─╯
5  temp-single-48520445580157.mp3


    audiobook_reencoder.main()   
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/audiobook_reencoder/audiobook_reencoder.py", line 1846, in main
    reencode_audio_file(logger, audio_file_data[os.path.join(dirpath,file_name)], file_count, total_count)
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/audiobook_reencoder/audiobook_reencoder.py", line 1247, in reencode_audio_file
    meta_status = add_metadata(logger, ffmpeg_output, audio_file_data, \
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/audiobook_reencoder/audiobook_reencoder.py", line 775, in add_metadata
    if imghdr.what(cover_art_filename) == 'png':
  File "/usr/lib/python3.8/imghdr.py", line 16, in what
    f = open(file, 'rb')
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/audiobook_reencode/80760304/5/9350730928675250.jpg'

