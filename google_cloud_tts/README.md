# google_cloud_tts

This is a script that allows you to convert a text file to mp3, read by Google Cloud's Text-to-Speech API.  It's pretty simple to use after you go though all the steps of setting up the Google Cloud account and Google's other requirements.

I personally found that Google's WaveNet TTS voices are the most realistic sounding voices out there.  As of 6/2019, you can use 1 million charators of wavelet voices for free.  After that its $14 per million charactors.  The general voices are not great, about average for TTS.  You can use 5 million charaters for free and $4 per millon after that.  This script will let you use ether one, by commenting and uncommenting a few varables at the top of the script.

### Usage
google-cloud-tts.sh [TEXT_FILE]

### Requirements
* ffmpeg
* Google Cloud SDK

#### Google Cloud account
* Create Google Cloud Platform project
* Enable the Cloud Text-to-Speech API
* Set up authentication key, and download json file
* Google Cloud Text-to-Speech: enabled
* Google application credential json file

### Installation
* Install required programs
* Copy 'google-cloud-tts.sh' to where ever you want it.
.* Add to $PATH if you want it.
* Download Google application credential json file
* Put the json file anywhere you want it.
* Edit 'google-cloud-tts.sh' and go to the configuration section
.* change 'GOOGLE_APPLICATION_CREDENTIALS="/home/bobthebuilder/google_cred.json"' to the location of your file
.* Comment out all voices you are not using. Only one voice is set at a time.
..* 'LANGUAGECODE, SPEACHVOICE, GENDER' are all required for each voice
..* You can find the available voices, as on 06/2019 in voice.txt or get an up to date list by executing
...* curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
"https://texttospeech.googleapis.com/v1/voices" > voices.txt



### Set up a Google Cloud acount and setup the TTS API
* General Steps
.* Create Google Cloud account
.* Create Google Cloud Platform project
.*	Enable the Cloud Text-to-Speech API
.*	Set up authentication key, and download json file
.*	Google Cloud Text-to-Speech: enabled
.*	Google application credential json file

* For detailed steps see:
.* https://cloud.google.com/text-to-speech/docs/quickstart-protocol


###	Useful tools:
* Calibre
.* ebook-convert zzzzzzz.epub zzzzzzz.txt


### Links
*		https://cloud.google.com/text-to-speech/
*		https://cloud.google.com/text-to-speech/docs/
*		https://cloud.google.com/text-to-speech/docs/quickstart-protocol
*		https://cloud.google.com/text-to-speech/quotas
*		https://cloud.google.com/text-to-speech/pricing

