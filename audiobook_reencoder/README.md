# audiobook_reencoder
* Description: Re-encodes all mp3/m4b files in a directory, and any directories.

* Features:
	* Works recursivly
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

# Default settings
most of these can be changed using command line flags or editing a little bit of the code
* bitrate: 32k
* samplerate: 22050Hz
* file format: mp3
* ID3 tags
	* Sets id3v2.3 and id3v1.1
	* genre: Audiobook
	* encoded_by: audiobook_reencoder(ffmpeg)-v0.1
	* embed image in same directory as ID3 cover art
	* Removes tags
		* compatible_brands
		* metadata minor_version
		* metadata major_brand
* Volume normalization: performed by 'ffmpeg -loudnorm'
* Extract embedded cover art to cover.jpg


# Usage Examples

## Re-encode all files in a directory
* python audiobook_reencoder.py DIRECTORY

## Set default bitrate, samplerate and/or audio format
by default bitrate=32k; samplerate=22050; format=mp3
* python audiobook_reencoder.py --bitrate 64k --samplerate 44100 --audio-output-format m4b DIRECTORY

## Embed cover art to each file in directory
* python audiobook_reencoder.py --only-extract-and-embed-cover-art DIRECTORY

## Delete unnessesary (cue/nfo/m3u) files
* python audiobook_reencoder.py --only-delete-unneeded-files DIRECTORY

## Delete all non-audio files 
* todo

## Delete all non-audio or non-image files 
* todo

## Split into chapters
* todo

# Useful external tools
* Audible-activator - extract your Audible authorization code (CLI)
	* <https://github.com/inAudible-NG/audible-activator>
* AAXtoMP3 - convert your Audible audiobooks to useful format ie. mp3, m4b (CLI)
	*  <https://github.com/KrumpetPirate/AAXtoMP3>
* inAudible - Convert Audible audiobooks to useful format ie. mp3, m4b (GUI, windows/mac only) <https://github.com/rmcrackan/inAudible>
* youtube-dl - Download videos (or audiobooks) from Youtube (CLI)
	* <https://youtube-dl.org/>
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
