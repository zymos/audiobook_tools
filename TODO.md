# Entire package
* create setup/install
  * copy to python dir
  * copy main exe to bin
  * make copy config to .config 
* create other package (deb, ...)
* Create seperate online-tts package (maybe)

#web-novel-tts (create)
* joining web-novel-to-text and online-tts

# web-novel-to-text
* add other web-novel sites
* remove non eu (needs fixed) change eu name to something
* command line arg service not woring
* check blank mp3 to show error
* remove non-latin1 charators option
  * https://stackoverflow.com/questions/23680976/python-removing-non-latin-characters
  * royalroad:text in a single line, which fails. needs to convert <br> to new line
* filenames with '='
* https://royalroad.com/fiction/39408/beware-of-chicken/chapter/684101/v2-c272 gives error text2digits
 
# online-tts
* remove_nonstandard_chars seems to be locked up for too much time
* implement profiles
* add amazion polly, ibm, google cloud support
* check timeout-retry (error response) maybe subsplit
* Bug: File does not exist shows as 0 files

# ab-reenconder
* Create temp dir per instance ?done?
* Add parallel process files
* test output m4b, ogg, opus
* *add cover art non mp3
* add option: remove all non-audio/image
* chapter title: if >99 chapter make 3-dig filename
* Bug
  * displays "keep originals," when not
  * chap with,~= 0 should be ignored: Done?
  * -new is moveing wrong thing
  * fix input bandwidth < output bandwidth: skip (FIXED)
  * no delete old
  * bitrate lower not good with m4b, check valid bitrate, check formate
  * lower bitrate doesnt copy cover art
  * force still skips


# notes
* icecream for debug?
