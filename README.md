# Audiobook Tools

These are some scripts to create and convert audiobooks.

### Tools

#### google-cloud-tts.sh
* Description: Creates audiobooks from ebooks using Google voice (text-to-speech)
*	Requirements:
	* ffmpeg
	* Google Cloud SDK
	* Calibre (ebooks to txt)

#### audiobook_reencoder
* Description: Re-encodes all mp3/m4b files in a directory, recursivly.
* Features:
	* Encodes using ffmpeg
    * Accepts mp3, m4b, m4a (todo maybe flac)
    * Grabs audio files data using ffprobe, for re-encoding and embedding cover art
    * Split into chapters (not implemented)
    * Removes unneeded files (nfo/cue/m3u) (can be disabled)
    * Add genre="Audiobook" (can be disabled)
    * Normalize volume (can be disabled)
	* Won't re-encode if it is obvious it has been done before (can be forced)
    * Cover art:
    	* Extracts cover art to cover.jpg (can be disabled)
		* Embeds cover art to each audiofile (can be disabled)
		* If directory contains multiple different audiobooks it won't try extract/embed cover art
		* Can delete original image file, after embedding (not default)
* Requirments
	* ffmpeg and ffprobe
	* python
```
usage: audiobook_reencoder.py [-h] [--disable-extract-cover-art]
                              [--disable-embed-cover-art]
                              [--only-extract-cover-art] [--disable-reencode]
                              [--only-reencode] [--disable-split-chapters]
                              [--disable-delete-unneeded-files]
                              [--only-delete-unneeded-files]
                              [--disable-add-id3-genre] [--only-add-id3-genre]
                              [--force-add-cover-art]
                              [--delete-image-file-after-adding]
                              [--audio-output-format AUDIO_OUTPUT_FORMAT]
                              [--bitrate BITRATE] [--samplerate SAMPLERATE]
                              [--threads THREADS] [--keep-original-files]
                              [--test] [--disable-normalize]
                              [--disable-add-id3-encoded-by] [--ignore-errors]
                              [--disable-id3-change] [--force-normalization]
                              [--debug]
                              directory

positional arguments:
  directory             directory to process

optional arguments:
  -h, --help            show this help message and exit
  --disable-extract-cover-art
                        Don't extract cover art from audio file to cover.jpg
  --disable-embed-cover-art
                        Don't add cover art
  --only-extract-cover-art
                        Only extract cover art to cover.jpg, no reencoding
  --disable-reencode    No reencoding
  --only-reencode       Only reencode
  --disable-split-chapters
                        Don't split chapters
  --disable-delete-unneeded-files
                        don't deletes nfo/cue/m3u files
  --only-delete-unneeded-files
                        Only delete nfo/cue/m3u file, no reencode
  --disable-add-id3-genre
                        Don't set ID3 tag genre=Audiobook
  --only-add-id3-genre  Don't re-encode, just add ID3 tag genre=Audiobook
  --force-add-cover-art
                        Ignores filename similarity ratio to decide weather to
                        add cover art
  --delete-image-file-after-adding
                        Delete image file from directory after adding it to
                        id3 as cover art (unimplimented)
  --audio-output-format AUDIO_OUTPUT_FORMAT
                        m4b or mp3 (default mp3)
  --bitrate BITRATE     8k, 16k, 32k, 64k, 128k, etc (default 32k)
  --samplerate SAMPLERATE
                        16000, 22050, 44100, etc (default 22050)
  --threads THREADS     number of CPU threads to use (default 4)(No Used Yet)
  --keep-original-files
                        do not delete original audio files
  --test                run without any action, extraction or reencoding
  --disable-normalize   do not normalize volume, faster encoding
  --disable-add-id3-encoded-by
                        Don't set ID3
                        encoded_by="audiobook_reencoder(ffmpeg)-v0.1"
  --ignore-errors       If there is an encoding failure, program will leave
                        the file as is, and continue processing the rest of
                        files
  --disable-id3-change  Don't change ID3 tags
  --force-normalization
                        Force re-encoder to normalize volume. By default,
                        ormalization is skipped if this encoder was likely run
                        previously on file
  --debug               prints debug info
```

#### audio_extract_cover_art
* Description: Extracts the cover art from mp3s, recursivly
* Requirments
	* ffmpeg


#### m4b split
* Desciption: Splits m4b files to chaptered mp3 files
* Requirements
	* ffmpeg
	* libmp4v2


#### wp post to ssml
* Description: Converts a Wordpress post to an SSML file to be used in a text-to-speech program or service.  This is useful for coverting web-novels to audio.
* Requirements
	* python
```
usage: wp-post-to-ssml.py [-h] [--format FORMAT] [-a] [-q] URL

positional arguments:
 URL                   URL to a Wordpress post

 optional arguments:
  -h, --help            show this help message and exit
	--format FORMAT       Format of each file
	-a, --speak-asterisk  Speaks out asterisk[*] (off by default)
	-q, --dont-remove-quotes    Leave quotes in place and may or may not be spoken    (off by default)
```

### Convert Youtube audiobooks to mp3 files
* Description: Downloads audiobooks from youtube
* Requirements:
	* youtube-dl
* Downloads single file
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 "[URL_GOES_HERE]"
* Downloads entire playlist: 
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 --yes-playlist "[URL_GOES_HERE]"
* Extracts cover art:  
	* youtube-dl --get-thumbnail "[URL_GOES_HERE]" | xargs wget -O cover.jpg
 
### Audible tools

#### Extract your Audible authorization code
* Description: Find your Audible 'activation byte', aka 'auth code', which is required for listening or converting your Audible audiobooks
* Download: <https://github.com/inAudible-NG/audible-activator>
* Notes: This tool requires Google Crome, but you can download Chrome and CromeDriver from the site, install it in a temp folder, adn delete it after.  Make sure the version of Chrome and CromeDriver are the same.

#### Convert Audible AAX files to mp3 (or other formats)
* Description: Convert **your** Audible audio book to a useful non-DRM format, default is chaptered mp3s, but it can do m4b and other formats
* Download: <https://github.com/KrumpetPirate/AAXtoMP3>
* Usage: AAXtoMP3 --authcode [YOUR_AUTH_CODE] [YOUR_AUDIBLE_FILE]
* Notes: If you want to use ffmpeg or avconv instead of AAXtoMP3, just use 'ffmpeg -activation_bytes [YOUR_AUTH_CODE] .....'

### Useful external tools
* id3v2 - MP3 ID3 tag command line editor (CLI)
	* <http://id3v2.sourceforge.net/>
* Calibre - ebook reader/converter (GUI and CLI)
	* <https://calibre-ebook.com/>
		* Ebook to txt: 'ebook-convert Book.epub Book.txt'
		* Extract cover art: ebook-meta --get-cover=cover.jpg
* EasyTag - MP3 ID3 tags GUI editor (GUI)
	* <https://sourceforge.net/projects/easytag/>
* puddletag - MP3 ID3 tags GUI editor (GUI)
	* <http://docs.puddletag.net/>
* Audible-activator - extract your Audible authorization code (CLI)
	* <https://github.com/inAudible-NG/audible-activator>
* AAXtoMP3 - convert your Audible audiobooks to useful format ie. mp3, m4b (CLI)
	*  <https://github.com/KrumpetPirate/AAXtoMP3>
* inAudible - Convert Audible audiobooks to useful format ie. mp3, m4b (GUI, windows only)
* youtube-dl - Download videos (or audiobooks) from Youtube (CLI)
	* <https://youtube-dl.org/>
* eyeD3 - ID3 editor with ability to add cover art
	* <https://eyed3.readthedocs.io/en/latest/>
