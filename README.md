# Audiobook Tools

These are some scripts to create and convert audiobooks.

### Tools

#### google-cloud-tts.sh
* Description: Creates audiobooks from ebooks using Google voice
*	Requirements:
	* ffmpeg
	* Google Cloud SDK
	* Calibre

#### audiobook_reencoder
* Description: Re-encodes all mp3/m4b files in a directories, extracts cover art, and some basic audiobook stuff
* Requirments
	* ffmpeg
	* id3v2

#### audio_extract_cover_art
* Description: Extracts the cover art from mp3s, recursivly
* Requirments
	* ffmpeg


#### m4b split
* Desciption: Splits m4b files to chaptered mp3 files
* Requirements
	* ffmpeg
	* libmp4v2

#### audiobook_youtube-dl
* Description: Downloads audiobooks from youtube
* Requirements:
	* youtube-dl
* Downloads single file
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 "URL_GOES_HERE"
* Downloads entire playlist: 
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 --yes-playlist "URL_GOES_HERE"
* Extracts cover art:  
	* youtube-dl --get-thumbnail "URL_GOES_HERE" | xargs wget -O cover.jpg
 


### Other useful external tools
* id3v2 - MP3 ID3 tag command line editor
* Calibre - ebook reader/converter
* easyTag - MP3 ID3 tags GUI editor
* puddletag - MP3 ID3 tags GUI editor

