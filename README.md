# Audiobook Tools - Command line tools

Description: A set of command line tools for creating, re-encoding and optimizing audiobooks


Includes
* Audiobook ReEncoder - bulk re-encode audiobook files to uniform format, with some bells and whistles
* Online TTS - Coverts Text-to-Speech audio files using various online TTS services
* Web-novel to Text - extracts web-novels from website and save to txt/ssml file


# Download

Release
* 0.01 - [zip file](https://github.com/zymos/audiobook_tools/archive/refs/tags/v0.01.zip), [tar.gz file](https://github.com/zymos/audiobook_tools/archive/refs/tags/v0.01.tar.gz)

Current snapshot
* Download: [zip file](https://github.com/zymos/audiobook_tools/archive/master.zip)
* Git: *git clone https://github.com/zymos/audiobook_tools.git*

# Install

* Install requirements
   * ffmpeg, python3
   * python modules: text2digits, imghd, PIL, mutagen
      * pip install Pillow, mutagen, text2digits, azure-cognitiveservices-speech
   * Optional: Google Cloud SDK, youtube-dl, Calibre, azure-cognitiveservices-speech
* Copy audiobook_tools folder where ever you want.
**   * Example: /opt/audiobook_tools
* Add directory to $PATH
   * Example: add PATH=$PATH:/opt/audiobook_tools to ~/.bashrc
* Use it


## Audiobook ReEncoder (audiobook_reencoder)
* Description: Bulk re-encodes all MP3/M4B files in a directory, recursivly.
* Features:
	* Encodes using ffmpeg
    * Accepts mp3, m4b, m4a, flac, ogg, opus, aax(with auth code)
    * Grabs audio files data using ffprobe, for re-encoding and embedding cover art
    * Split into chapters (optional)
    * Removes unneeded files (nfo/cue/m2u) (optional)
    * Add genre="Audiobook" (optional, default)
    * Normalize volume (optional, default)
	* Won't re-encode if it is obvious it has been done before (optional, default)
    * Cover art:
    	* Extracts cover art to cover.jpg (optional)
		* Embeds cover art to each audiofile (optional, default)
		* If directory contains multiple different audiobooks it won't try extract/embed cover art
		* Can delete original image file, after embedding (optional)
* Requirments
	* ffmpeg and ffprobe
	* python3
* [more details](https://github.com/zymos/audiobook_tools/tree/master/docs/audiobook_reencoder.md)


## Online TTS (online-tts)
* Description: Text-to-Speech program using online/cloud TTS services.
* Supported service
  * not supported yet: Google Cloud SDK (requires Google Cloud SDK)
  * Microsoft Azure TTS (reqires azure-cognitiveservices-speech)
  * VoiceRSS TTS
  * Google translate TTS (not Google cloud TTS)
  * Easy to add other TTS APIs
* [more details](https://github.com/zymos/audiobook_tools/tree/master/docs/online_tts.md)



## Web-Novel to Text (web-novel-to-text)
* Description: Extracts the text of web-novels articles/chapters to a TXT or SSML file to be used in a text-to-speech program or service.
* Supported Sites
  * Royal Road
  * WordPress sites
  * TODO: add more
* Requirements
  * python3
    * python module: text2digits
* [more details](https://github.com/zymos/audiobook_tools/tree/master/docs/web_novel_to_text.md)


## AAX Converter (aaxconverter)
* Description: convert AAX(Audible) files to mp3, m4b, single or chapter files, removing DRM.  This almost a copy of KrumpetPirate's [AAXtoMP3](https://github.com/KrumpetPirate/AAXtoMP3)
* [more details](https://github.com/zymos/audiobook_tools/tree/master/docs/aaxconverter.md)


## Other tools
### google-cloud-tts.sh
* Description: Creates audiobooks from ebooks using Google voice (text-to-speech)
*	Requirements:
	* ffmpeg
	* Google Cloud SDK
* [more details](https://github.com/zymos/audiobook_tools/tree/master/audiobook_tools/google_cloud_tts)



# Recomneded External Programs

### Calibre (external)
* ebook reader/converter (GUI and CLI)
* <https://calibre-ebook.com/>
	* Ebook to txt: 'ebook-convert Book.epub Book.txt'
	* Extract cover art: ebook-meta --get-cover=cover.jpg

### youtube-dl: Convert Youtube audiobooks to mp3 files (external)
* Description: There are many audiobooks on youtube.  Mostly web-novels and light-novels read by computers, that will likely never be produced in studios.
* Usage: download single file
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 "[URL_GOES_HERE]"
* Usage: download entire playlist: 
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 --yes-playlist "[URL_GOES_HERE]"
* Usage: extract cover art:  
	* youtube-dl --get-thumbnail "[URL_GOES_HERE]" | xargs wget -O cover.jpg
* Download : <https://youtube-dl.org/>
* Git: <https://github.com/ytdl-org/youtube-dl>

### Mycroft Mimic TTS (external)
* Description: Free TTS for running on your computer, better than festival or espeak
	* <https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-overview>


### inAudible-NG/audible-activator: Extract your Audible authorization code (external)
* Description: Find your Audible 'activation byte', aka 'auth code', which is required for listening or converting your Audible audiobooks
* Download: <https://github.com/inAudible-NG/audible-activator>
* Notes: This tool requires Google Crome, but you can download Chrome and CromeDriver from the site, install it in a temp folder, adn delete it after.  Make sure the version of Chrome and CromeDriver are the same.

### AAXtoMP3: Convert Audible AAX files to mp3 (or other formats) (external)
* Description: Convert **your** Audible audio book to a useful non-DRM format, default is chaptered mp3s, but it can do m4b and other formats
* Download: <https://github.com/KrumpetPirate/AAXtoMP3>
* Usage: AAXtoMP3 --authcode [YOUR_AUTH_CODE] [YOUR_AUDIBLE_FILE]
* Notes: If you want to use ffmpeg or avconv instead of AAXtoMP3, just use 'ffmpeg -activation_bytes [YOUR_AUTH_CODE] .....'

## Other useful tools (external)
* Audible-activator - extract your Audible authorization code (CLI)
	* <https://github.com/inAudible-NG/audible-activator>
* inAudible - Convert Audible audiobooks to useful format ie. mp3, m4b (GUI, windows/mac only) <https://github.com/rmcrackan/inAudible>
* ffmpeg - video/audio converter/encoder <https://ffmpeg.org/>
* MP3 error checking
	* mpck <http://checkmate.gissen.nl/>
	* mp3diag <http://mp3diags.sourceforge.net/>
	* mp3check <https://sourceforge.net/projects/mp3check/>
	* mp3val <http://mp3val.sourceforge.net/>
	* mp3guessenc <https://mp3guessenc.sourceforge.io/>
* MP3 ID3 tag
	* id3v2  <http://id3v2.sourceforge.net/>
	* exiftool <https://exiftool.org/>
	* EasyTag - MP3 ID3 tags GUI editor (GUI) <https://sourceforge.net/projects/easytag/>
	* puddletag - MP3 ID3 tags GUI editor (GUI) <http://docs.puddletag.net/>
* MP3 info tool
	* mp3guessenc <https://mp3guessenc.sourceforge.io/>
	* eyeD3 <https://eyed3.readthedocs.io/en/latest/>
	* ffprobe, part of ffmpeg <https://ffmpeg.org/>
	* mediainfo: <https://mediaarea.net/en/MediaInfo>
