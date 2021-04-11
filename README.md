# Audiobook Tools

Description: A set of CLI tools for creating and optimizing audiobooks

audiobook-reencoder
* re-encoding your audiobooks to the same format, and options

online-tts
* converting text-to-speech using online/cloud TTS services

web-novel-to-text
* extracting web-novel chapters from websites and saving to TXT or SSML

aaxconverter
* convert AAX files to MP3 or M4B, removing DRM


* Requirements:
	* python
	* ffmpeg
    * See below for required modules




Download tools: [zip file](https://github.com/zymos/audiobook_tools/archive/master.zip)

Git: *git clone https://github.com/zymos/audiobook_tools.git*




# audiobook_reencoder
* Description: Re-encodes all MP3/M4B files in a directory, recursivly.
* Features:
	* Encodes using ffmpeg
    * Accepts mp3, m4b, m4a 
    * Grabs audio files data using ffprobe, for re-encoding and embedding cover art
    * Split into chapters (not implemented)
    * Removes unneeded files (nfo/cue/m2u) (can be disabled)
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
* [more details](https://github.com/zymos/audiobook_tools/tree/master/audiobook_reencoder)


# online-tts
* Description
<pre>
usage: online-tts [-h] [--bitrate {32k,48k,64k,96k,128k,196k}]
                  [--samplerate {16000,22050,44100,48000}] [--format {mp3,wav,ogg}]
                  [--input-format {txt,ssml,json-txt,json-ssml}] [--key KEY]
                  [--locale LOCALE] [--voice VOICE] [--gender GENDER]
                  [--url_parameters URL_PARAMETERS]
                  [--audio_settings AUDIO_SETTINGS] [--gtts-lang GTTS_LANG]
                  [--gtts-tld GTTS_TLD] [--tts-service TTS_SERVICE]
                  [--profile PROFILE] [--dont_remove_asterisk]
                  [--dont_remove_quotes]
                  EBOOK [EBOOK ...]

positional arguments:
  EBOOK                 ebook txt file

optional arguments:
  -h, --help            show this help message and exit
  --bitrate {32k,48k,64k,96k,128k,196k}
                        audio encoding bitrate
  --samplerate {16000,22050,44100,48000}
                        audio encoding samplerate
  --format {mp3,wav,ogg}
                        audio encoding format
  --input-format {txt,ssml,json-txt,json-ssml}
                        format sent to TTS service
  --key KEY             key, auth code, auth file
  --locale LOCALE       example: en-us, en-au,
  --voice VOICE         voice
  --gender GENDER
  --url_parameters URL_PARAMETERS
                        this will be attached to url after question mark
  --audio_settings AUDIO_SETTINGS
  --gtts-lang GTTS_LANG
                        language for google-translate-tts
  --gtts-tld GTTS_TLD   top-level-domain for google-tanslate-tts accents
  --tts-service TTS_SERVICE
                        tts service to use. ie google_translate_tts, voicerss,
                        google_cloud_tts(unimplemented), amazone_polly(unimplemented
  --profile PROFILE     profile to use, set in config file
  --dont_remove_asterisk
                        Some TTS servers speak out "asterisk", by default they are
                        removed
  --dont_remove_quotes  Some TTS servers speak out "quote", by default they are
                        removed
</pre>


# web-novel-to-text
* Description: Extracts web-novels to a TXT or SSML file to be used in a text-to-speech program or service.
<pre>
usage: web-novel-to-text [-h] [--format {txt,ssml,json}] [-a] [-q]
                         [--dont-emphasize] [--output-format OUTPUT_FORMAT]
                         INPUT

Converts a post to a txt or ssml file.

positional arguments:
  INPUT                 URL of post or file with list of URLs

optional arguments:
  -h, --help            show this help message and exit
  --format {txt,ssml,json}
                        Format to output (json stores metadata)
  -a, --speak-asterisk  Speaks out asterisk[*] (off by default)
  -q, --dont-remove-quotes
                        Leave quotes in place and may or may not be spoken (off by
                        default)
  --dont-emphasize      Don't use emphasize tag in ssml
  --output-format OUTPUT_FORMAT
                        filename to output

</pre>

# aaxconverter (opus, ogg may not work)
<pre>
Usage: aaxconverter [--flac] [--aac] [--opus ] [--single] [--chaptered]
[-e:mp3] [-e:m4a] [-e:m4b] [--authcode <AUTHCODE>] [--no-clobber]
[--target_dir <PATH>] [--complete_dir <PATH>] [--validate]
{FILES}
</pre>

# Other tools
## google-cloud-tts.sh
* Description: Creates audiobooks from ebooks using Google voice (text-to-speech)
*	Requirements:
	* ffmpeg
	* Google Cloud SDK
* [more details](https://github.com/zymos/audiobook_tools/tree/master/google_cloud_tts)


## m4b split
* Desciption: Splits m4b files to chaptered mp3 files
* Requirements
	* ffmpeg
	* libmp4v2
* [more details](https://github.com/zymos/audiobook_tools/tree/master/m4b_split)



# Recomneded External Programs

## Calibre (external)
* ebook reader/converter (GUI and CLI)
* <https://calibre-ebook.com/>
	* Ebook to txt: 'ebook-convert Book.epub Book.txt'
	* Extract cover art: ebook-meta --get-cover=cover.jpg

## youtube-dl: Convert Youtube audiobooks to mp3 files (external)
* Description: There are many audiobooks on youtube.  Mostly web-novels and light-novels read by computers, that will likely never be produced in studios.
* Usage: download single file
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 "[URL_GOES_HERE]"
* Usage: download entire playlist: 
	* youtube-dl --extract-audio --embed-thumbnail --add-metadata --audio-format mp3 --yes-playlist "[URL_GOES_HERE]"
* Usage: extract cover art:  
	* youtube-dl --get-thumbnail "[URL_GOES_HERE]" | xargs wget -O cover.jpg
* Download : <https://youtube-dl.org/>
* Git: <https://github.com/ytdl-org/youtube-dl>

## Mycroft Mimic TTS (external)
* Description: Free TTS for running on your computer, better than festival or espeak
	* <https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-overview>


## inAudible-NG/audible-activator: Extract your Audible authorization code (external)
* Description: Find your Audible 'activation byte', aka 'auth code', which is required for listening or converting your Audible audiobooks
* Download: <https://github.com/inAudible-NG/audible-activator>
* Notes: This tool requires Google Crome, but you can download Chrome and CromeDriver from the site, install it in a temp folder, adn delete it after.  Make sure the version of Chrome and CromeDriver are the same.

## AAXtoMP3: Convert Audible AAX files to mp3 (or other formats) (external)
* Description: Convert **your** Audible audio book to a useful non-DRM format, default is chaptered mp3s, but it can do m4b and other formats
* Download: <https://github.com/KrumpetPirate/AAXtoMP3>
* Usage: AAXtoMP3 --authcode [YOUR_AUTH_CODE] [YOUR_AUDIBLE_FILE]
* Notes: If you want to use ffmpeg or avconv instead of AAXtoMP3, just use 'ffmpeg -activation_bytes [YOUR_AUTH_CODE] .....'



# Other useful tools (external)
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
