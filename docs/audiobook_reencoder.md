# Audiobook ReEncoder

## Description:
Re-encodes all MP3/M4B files in a directory, recursivly.

## Features:
	- Encodes using ffmpeg
    - Accepts mp3, m4b, m4a 
    - Grabs audio files data using ffprobe, for re-encoding and embedding cover art
    - Split into chapters (not implemented)
    - Removes unneeded files (nfo/cue/m2u) (can be disabled)
    - Add genre="Audiobook" (can be disabled)
    - Normalize volume (can be disabled)
	- Won't re-encode if it is obvious it has been done before (can be forced)
    - Cover art:
    	- Extracts cover art to cover.jpg (can be disabled)
		- Embeds cover art to each audiofile (can be disabled)
		- If directory contains multiple different audiobooks it won't try extract/embed cover art
		- Can delete original image file, after embedding (not default)

## Requirments
	- ffmpeg and ffprobe
	- python

## Usage
<pre>
usage: audiobook-reencoder [-h] [--disable-extract-cover-art]
                           [--disable-embed-cover-art] [--only-extract-cover-art]
                           [--disable-reencode] [--only-reencode]
                           [--disable-split-chapters]
                           [--disable-delete-unneeded-files]
                           [--only-delete-unneeded-files] [--disable-add-id3-genre]
                           [--only-add-id3-genre] [--force-add-cover-art]
                           [--delete-image-file-after-adding]
                           [--audio-output-format AUDIO_OUTPUT_FORMAT]
                           [--bitrate BITRATE] [--samplerate SAMPLERATE]
                           [--threads THREADS] [--keep-original-files] [--test]
                           [--disable-normalize] [--disable-add-id3-encoded-by]
                           [--ignore-errors] [--disable-id3-change]
                           [--force-normalization] [--delete-non-audio-files]
                           [--delete-non-audio-image-files] [--debug]
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
                        Ignores filename similarity ratio to decide weather to add
                        cover art
  --delete-image-file-after-adding
                        Delete image file from directory after adding it to id3 as
                        cover art (unimplimented)
  --audio-output-format AUDIO_OUTPUT_FORMAT
                        m4b or mp3 (default mp3)
  --bitrate BITRATE     8k, 16k, 32k, 64k, 128k, etc (default 32k)
  --samplerate SAMPLERATE
                        16000, 22050, 44100, etc (default 22050)
  --threads THREADS     number of CPU threads to use (default 4)
  --keep-original-files
                        do not delete original audio files
  --test                run without any action, extraction or reencoding
  --disable-normalize   do not normalize volume, faster encoding
  --disable-add-id3-encoded-by
                        Don't set ID3 encoded_by="audiobook_reencoder(ffmpeg)-v0.1"
  --ignore-errors       If there is an encoding failure, program will leave the file
                        as is, and continue processing the rest of files
  --disable-id3-change  Don't change ID3 tags
  --force-normalization
                        Force re-encoder to normalize volume. By default,
                        normalization is skipped if this encoder was likely run
                        previously on file
  --delete-non-audio-files
                        Delete all non-audio files(not implemented yet)
  --delete-non-audio-image-files
                        Delete all non-audio, or non-image files(not implemented
                        yet)
  --debug               prints debug info
</pre>

## Feature Descriptions

- Input/Output files/directories
   - Input: single file or directory
   - for directory input, searches directory recursivly
   - Input: mp3, m4b, m4a 
   - Output: mp3, (m4b, ogg, opus untested)
   - Overwrite original file (default) or keep copy of original file (optional)
   - Checks if file has already been encoded, and skips (default, optional)
      - Won't re-encode if it is obvious it has been done before (can be forced) 
      - this program leaves metadata tag in encoded_by='audiobook_reencoder(ffmpeg)-v0.1'


- Encoding options
   - checks bitrate and won't reencode at higher bitrate or samplerate
   - valid_bitrates = ['8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k']
   - valid_bandwidths = ['8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000']
   - ffmpeg command used: FFREPORT="file=/tmp/audiobook_reencode/audiobook_reencode-log-22y02m14d-12-59/ffmpeg_output/XXXXXXX.m4b.0.log:level=40" ffmpeg   -loglevel error -y -i "YYYYYYY/XXXXXXX.m4b" -c:a libmp3lame -b:a 48k -ar 22050 -filter:a loudnorm=I=-17  -id3v2_version 3 -write_id3v1 1 -metadata compatible_brands= -metadata minor_version= -metadata major_brand= -metadata iTunSMPB= -map_chapters -1  "/tmp/audiobook_reencode/89059725/YYYYYYY/temp-single-71368559944577.mp3"


- Split into chapters into individual files(default, optional)

- Removes unneeded files (nfo/cue/m2u) (optional)

- Metadata/ID3
   - Add genre="Audiobook" (default, optional)
      - media_type=2 for m4b/mp4 (ie Audiobook)
   - removes leftover entries
      -  compatible_brands= minor_version= major_brand= iTunSMPB=
   - Cover art:
    	- Extracts cover art to cover.jpg (can be disabled)
		- Embeds cover art to each audiofile (default, optional)
		- If directory contains multiple different audiobooks it won't try extract/embed cover art
         - uses fuzzy search to compare files names, and won't do anything if not similar
		- Can delete original image file, after embedding (not default)            (Unchecked)
      - Grabs audio files data using ffprobe, for re-encoding and embedding cover art

- Options priority
   - command line args -> local config file -> config file in packages config directory
   - package config location: audiobook_tools/config_files/
   - local config location: 
      - Linux ~/.config/audiobook-tools/audiobook-reencoder.conf
      - Windows: 
      - OSX:

- Volume normalize (default, optional)
   - Uses ffmpeg's loudnorm, an R128 normalize, but increases level to -17dB to match levels used by most audiobooks

- Verbose log file for debuging and tracking down encoding 
   - writen to systems tmp dir
   - example: /tmp/audiobook_reencode/audiobook_reencode-log-22y02m14d-12-59.log   

- CLI output 
   - estimates encoding time
   - displays encoding progress
   - prints final encoding status=success/failed/skipped for each file

