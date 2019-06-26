#!/bin/bash


################################################################
# google-cloud-tts.sh
#
#	Author: ZyMOS
#	Date: 07/2019
#	License: GPLv3
#
#	Usage: google-cloud-tts.sh [TEXT_FILE]
#
#	Requirements:
#		ffmpeg
#		Google Cloud SDK
#		Google Cloud account
#			Create Google Cloud Platform project
#			Enable the Cloud Text-to-Speech API
#			Set up authentication key, and download json file
#			Google Cloud Text-to-Speech: enabled
#			Google application credential json file
#
#	Useful links:
#		https://cloud.google.com/text-to-speech/
#		https://cloud.google.com/text-to-speech/docs/
#		https://cloud.google.com/text-to-speech/docs/quickstart-protocol
#		https://cloud.google.com/text-to-speech/quotas
#		https://cloud.google.com/text-to-speech/pricing
#
#	Notes:
#		Standard (non-WaveNet) voices < 4 million characters free
#		WaveNet voices < 1 million characters free
#		Max characters per request < 5,000; shorter requests give less errors
#		
#	Useful tools:
#		Calibre
#			ebook-convert zzzzzzz.epub zzzzzzz.txt
#


########################################################################################
# Configure
#

###############################
# Google credential json file
GOOGLE_APPLICATION_CREDENTIALS="/home/zymos/Downloads/starbook6-aac17460d6ba.json"


###############################
# Voices
# 	run the following command to find available voices
# 		curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#  	 	-H "Content-Type: application/json; charset=utf-8" \
#  		"https://texttospeech.googleapis.com/v1/voices" > voices.txt

# Wavenet voice (better, but more expensive, <1M free)
# LANGUAGECODE='en-US'
# SPEACHVOICE='en-US-Wavenet-A'
# GENDER='MALE'

# Basic voice
LANGUAGECODE='en-US'
SPEACHVOICE='en-US-Standard-B'
GENDER='MALE'

SPEAKINGRATE='0.95' # 1 is default


####################
# MP3 info
BITRATE="32k"



##########################################################################################
##########################################################################################
## Code
##



# Variables
SYNTHTXT="synthesize-text.txt"
SYNTHAUD="synthesize-aud.mp3"
SPLITSIZE=1000

# Check arg/input file
BOOKNAME=$1
if [ -z "$1" ]; then
	echo "Error: ARG is not a file"
	echo "Usage: google-cloud-tts.sh [TEXT_FILE]"
	exit 1
fi
if ! [[ $(file -0 "$BOOKNAME" | cut -d $'\0' -f2 | grep text) ]]; then
	echo "Error: File is not a text file"
	echo "Usage: google-cloud-tts.sh [TEXT_FILE]"	
	exit 1
fi
if ! [ -f "$BOOKNAME" ]; then
	echo "Error: ARG is not a file"
	echo "Usage: google-cloud-tts.sh [TEXT_FILE]"
	exit 1
fi

# create absolute path
if ! [[ "$BOOKNAME" = /* ]]; then
	BOOKNAME="$(pwd)/$BOOKNAME"
fi


# Use getopts for arguments (unimpleneted)
# while getopts u:d:p:f: option
# do
	# case "${option}"
	# in
		# u) USER=${OPTARG};;
		# d) DATE=${OPTARG};;
		# p) PRODUCT=${OPTARG};;
		# f) FORMAT=$OPTARG;;
	# esac
# done

# Set output file
OUTPUTFILE=$(echo "$BOOKNAME"|sed 's/\.txt/.mp3/')


# Starting
echo "Converting: $BOOKNAME"
echo "	Output: $OUTPUTFILE"

# Generate tmp dirs
mkdir -p tmp
mkdir -p tmp/bak
mv tmp/* tmp/bak/ &> /dev/null
# $(rm tmp/*.*)
cd tmp

# import credentals file
export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS


# split into 5000 max charator files, google limit per request, less lines, gives less errors
split -C $SPLITSIZE -a 4 --numeric-suffixes=0 --additional-suffix=".txt" "$BOOKNAME" SECTION

# Display section counts
SECTIONSLIST=(SECTION*.txt)
SECTIONCOUNT=`echo "${SECTIONSLIST[@]: -1}" | sed 's/SECTION//'|sed 's/\.txt//'`
echo "Split into sections: $SECTIONCOUNT"

echo -n "Converting."
# Encoding text section to audio
for FILENAME in $(ls SECTION*)
do
	# echo "Converting: $FILENAME"
	echo -n "."
	TEXT="`cat $FILENAME | sed 's/['\''’‘´\`]/’/g'`" # remove posible inconsistent quote problems
	# printf -v TEXT "%q" "`cat $FILENAME`" #remove any prob with quotes
	# TEXT="`cat $FILENAME| tr -dc '[:alnum:]\n\r'`"
	echo $TEXT > "$FILENAME-text-sent.txt" # for debuging

	# Sends text to google and returns audio
	# speaking_rate
	TRY=0
	while [ $TRY -le 2 ]; do
		curl -s -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
		  -H "Content-Type: application/json; charset=utf-8" \
	  --data "{
		'input':{
		  'text':'$TEXT'
		},
		'voice':{
		  'languageCode':'$LANGUAGECODE',
		  'name':'$SPEACHVOICE',
		  'ssmlGender':'$GENDER'
		},
		'audioConfig':{
		  'audioEncoding':'MP3',
		  'speakingRate':'$SPEAKINGRATE'
		}
		}" "https://texttospeech.googleapis.com/v1/text:synthesize" > $FILENAME$SYNTHTXT

		# detect failures
		if [ $(cat $FILENAME$SYNTHTXT|grep 'error') ]; then 
			TRY=$(( $TRY + 1))
			echo "\nError detected in: $FILENAME, Try $TRY"
		else
			TRY=10 # All is good
		fi
	done
	
	# Failed too many times, exit
	if [ $TRY -ne 10 ]; then 
		echo "\n----------------------------"
		cat $FILENAME$SYNTHTXT
		echo "----------------------------"
		echo " See: https://cloud.google.com/speech-to-text/docs/reference/rpc/google.rpc"
		exit 1
	fi

	# convert output to mp3
	cat $FILENAME$SYNTHTXT | grep 'audioContent' | \
		sed 's|audioContent| |' | tr -d '\n ":{},' > tmp.txt && \
		base64 tmp.txt --decode > $FILENAME$SYNTHAUD && \
		rm tmp.txt
done



# Joins audio sections to single file
if ! [ $(cat *.mp3 | ffmpeg -y -loglevel 8 -i - -b:a $BITRATE "$OUTPUTFILE") ]; then
	echo
	echo "Success: $OUTPUTFILE"
	exit 0
else
	echo
	echo "Error: merging sections failed"
	echo "	Command: cat *.mp3 | ffmpeg -y -loglevel 8 -i - -b:a $BITRATE \"$OUTPUTFILE\""
	exit 1
fi


exit 0
