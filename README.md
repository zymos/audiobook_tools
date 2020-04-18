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
		  *	Won't re-encode if it is obvious it has been done before (can be forced)
          * Cover art:
              * Extracts cover art to cover.jpg (can be disabled)
              * Embeds cover art to each audiofile (can be disabled)
              * If directory contains multiple different audiobooks it won't try extract/embed cover art
              * Can delete original image file, after embedding (not default)

* Requirments
	* ffmpeg and ffprobe
	* python

#### audio_extract_cover_art
* Description: Extracts the cover art from mp3s, recursivly
* Requirments
	* ffmpeg


#### m4b split
* Desciption: Splits m4b files to chaptered mp3 files
* Requirements
	* ffmpeg
	* libmp4v2

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
