# Web Novel to Text

## Description: 
Text-to-Speech program using online/cloud TTS services.

## Usage
<pre>
usage: web-novel-to-text [-h] [-a] [-q] [--keep-problematic-chars]
                         [--disable-emphasize] [--debug] [--test]
                         [--format {txt,ssml,json}]
                         [--first-file-number FIRST_FILE_NUMBER]
                         [--output-filename OUTPUT_FILENAME]
                         INPUT

Converts a post to a txt/ssml file.

positional arguments:
  INPUT                 URL of post or file with list of URLs

optional arguments:
  -h, --help            show this help message and exit
  -a, --keep-asterisk   Speaks out asterisk[*] (off by default)
  -q, --keep-quotes     leave double quotes in place and may or may not be spoken
                        (off by default)
  --keep-problematic-chars
                        don\'t removes problematic charactors, that are often spoken
                        [\"\\\/*]
  --disable-emphasize   don't emphasize some text in ssml
  --debug               debug mode, more output
  --test                test mode, no writing data
  --format {txt,ssml,json}
                        Format to output (json stores metadata, txt and ssml)
  --first-file-number FIRST_FILE_NUMBER
                        number for first output file's name, each additional file
                        will increment this number, useful for keeping output files
                        in order
  --output-filename OUTPUT_FILENAME
                        filename to output, can be dynamic, see below

Output filename can be dynamic, using variables extracted from webpage. 
    %a - author
    %b - book title
    %t - chapter title
    %n - chapter number (extracted from chapter title, may not be reliable)
    %N - chapter number (three digits w/ leading zeros, extracted from chapter title, may not be reliable)
    %c - incremental count (starting with "--start-number", increments for each link in file)
    %F - publication date YYYY-MM-DD
    %T - publication time HH:MM:SS
    Example: "%b - Chapter %N" -> "Moby Dick - Chapter 003"
</pre>

## Changelog
- set default format from ssml to txt

