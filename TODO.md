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
* error
<p>“劳驾—”</p>
<pre>
Processing URL: https://wanderinginn.com/2020/06/14/7-29-b/
Traceback (most recent call last):
  File "/home/zymos/Documents/working-dirs/audiobook_tools/web-novel-to-text", line 12, in <module>
    web_novel_to_text.main()
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/web_novel_to_text/web_novel_to_text.py", line 857, in main
    file = process_url(url.rstrip())
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/web_novel_to_text/web_novel_to_text.py", line 740, in process_url
    (content, meta) = extract_txt_wordpress(site_code)
  File "/home/zymos/Online Storage/Zoho Docs/Documents/working-dirs/audiobook_tools/audiobook_tools/web_novel_to_text/web_novel_to_text.py", line 543, in extract_txt_wordpress
    article_html += str(etree.tostring(line).decode('utf-8'))
  File "src/lxml/etree.pyx", line 3435, in lxml.etree.tostring
  File "src/lxml/serializer.pxi", line 139, in lxml.etree._tostring
  File "src/lxml/serializer.pxi", line 199, in lxml.etree._raiseSerialisationError
lxml.etree.SerialisationError: IO_ENCODER
</pre>

# online-tts
* remove_nonstandard_chars seems to be locked up for too much time
* implement profiles
* add amazion polly, ibm, google cloud support
* check timeout-retry
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
