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
#		base64
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
GOOGLE_APPLICATION_CREDENTIALS_DEFAULT="$HOME/.auth/google.json"


###############################
# Voices
# 	run the following command to find available voices
# 		curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#  	 	-H "Content-Type: application/json; charset=utf-8" \
#  		"https://texttospeech.googleapis.com/v1/voices" > voices.txt
#
# All 3 variables required to match google's specific voice, comment out all voices not used
#
# 	List of voices:
#		https://cloud.google.com/text-to-speech/docs/voices
#
#
# Wavenet voice (better, but more expensive, <1M free)


# Basic male voice
SPEACHVOICE_DEFAULT_MALE='en-US-Standard-B'


# Basic female voice
LANGUAGECODE_DEFAULT='en-US'
SPEACHVOICE_DEFAULT='en-US-Standard-C'
GENDER_DEFAULT='FEMALE'

# Best female voice
# LANGUAGECODE='en-US'
# SPEACHVOICE='en-US-Wavenet-F'
# GENDER='FEMALE'

SPEAKINGRATE='0.95' # 1 is default


####################
# MP3 info
BITRATE="32k"

###################
# Debuging
DELETETMPFILES=0






##########################################################################################
##########################################################################################
## Code
##



# Variables
SYNTHTXT="synthesize-text.txt"
SYNTHAUD="synthesize-aud.mp3"
SPLITSIZE=1000
# create absolute path
if ! [[ "$BOOKNAME" = /* ]]; then
	BOOKNAME="$(pwd)/$BOOKNAME"
fi
echo "b: $BOOKNAME"
function usage_function {
	echo "Usage: google-cloud-tts.sh [--ssml] [--gender GENDER] [--voice-name VOICE_NAME] [--google-auth-file JSON_FILE] [--output FILENAME] [--language-code LOCALE] TEXT_OR_SSML_FILE"
	echo
	echo "	--ssml  	(optional)"
	echo "		:input file is an ssml file"
	echo "	-o, --output FILENAME 		(optional)"
	echo "		:assigns the filename to save as"
	echo "	--gender GENDER		(optional)"
	echo "		:male or female"
	echo "			 default: female"
	echo "	--voice-name VOICE_NAME  		(optional)"
	echo "		:google's voice name"
	echo "		 	default: $SPEACHVOICE_DEFAULT"
	echo "		 	default(male): $SPEACHVOICE_DEFAULT_FEMALE"
	echo "			See: https://cloud.google.com/text-to-speech/docs/voices"
	echo "	--language-code LOCALE 		(optional)"
	echo "		: language code (default $LANGUAGECODE_DEFAULT"
	echo "	--google-auth-file JSON_FILE  		(required, if Env Var not set)"
	echo "		:location of Google's json credential file "
	echo "			 default location: $GOOGLE_APPLICATION_CREDENTIALS_DEFAULT"
	echo "			 or set in env var: \$GOOGLE_APPLICATION_CREDENTIALS"
	echo
	# echo "				echo "	-						:input is STDIN, and can be piped in"
	# echo $0
}






# Assign defaults
SSML=0
OUTPUT_FILE_ASSIGNED=0
LANGUAGECODE=$LANGUAGECODE_DEFAULT
SPEACHVOICE=$SPEACHVOICE_DEFAULT
GENDER=$GENDER_DEFAULT
GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS_DEFAULT"


while true; do
  case "$1" in
    # Use SSML not text file
    -s | --ssml   	) SSML=1;          shift ;;

	# Assign output filename
	-o | --output	) OUTPUT_FILE_ASSIGNED=1
					OUTPUT_FILENAME_ASSIGNED="$2"
					shift
					shift
					;;
    
	# Command synopsis.
    -h | --help     ) usage_function ;     exit ;;
	
	# Google's voice name
	--voicename		) SPEACHVOICE="$2"
					shift
					shift
					;;
    
	# Gender (male or female)
	--gender		) GENDER="$2"
					shift
					shift
					;;
	--google-auth-file )
					GOOGLE_APPLICATION_CREDENTIALS="$2"
					shift
					shift
					;;
	# Anything else should be input file, but we will check
    *               )
					BOOKNAME=$1
                    break ;;
  esac
done

GOOGLE_APPLICATION_CREDENTIALS=`dirname $GOOGLE_APPLICATION_CREDENTIALS`/`basename $GOOGLE_APPLICATION_CREDENTIALS`


# ERROR Checks
# -----
# no args set
if [ "$#" -eq 0 ]; then
  usage_function
  exit 1
fi
# google cred file not found
if ! [ -f $GOOGLE_APPLICATION_CREDENTIALS ]; then
	if ! [ -f $GOOGLE_APPLICATION_CREDENTIALS_DEFAULT ]; then
		echo "Error: Google Cloud credential file does not exist or is not set"
		echo "Set json credential file's location to environment variable"
		echo "export GOOGLE_APPLICATION_CREDENTIALS=[files_location]"
		echo "or is located in $GOOGLE_APPLICATION_CREDENTIALS_DEFAULT"
		echo "See for details: https://console.cloud.google.com/apis/credentials"
		echo
		usage_function
		exit 1
	fi
fi
# ffmpeg not found
if ! [[ `which ffmpeg` ]]; then
  echo "ERROR ffmpeg is not installed"
  echo "Without it, this script will break."
  echo
  usage_function
  exit 1
fi
# gcloud is not installed
if ! [[ `which gcloud` ]]; then
  echo "ERROR: gcloud was not installed"
  echo "Without it, this script will break."
  echo
  usage_function
  exit 1
fi

# other requirements not found
if ! [[ `which bash` || `which pwd` || `which readline` || `which dirname` || `which mktemp` || `which split` || `which type` || `which cut` || `which file` || `which grep` || `which base64` ]]; then
  echo "ERROR: the following programs are required, they are usually preinstalled on"
  echo "most systems."
  echo "Requirements: bash, pwd, readline, dirname, mktemp, split, type, cut, file, grep, base64, echo, sed"
  echo
  usage_function
  exit 1
fi
# book file has a prob
if [ -z "$BOOKNAME" ]; then
	echo "Error: \"$BOOKNAME\" is not a file"
	echo
	usage_function
	exit 1
fi
if ! [[ $(file -0 "$BOOKNAME" | cut -d $'\0' -f2 | grep text) ]]; then
	echo "Error: \"$BOOKNAME\" is not a text file"
	echo
	usage_function	
	exit 1
fi
if ! [ -f "$BOOKNAME" ]; then
	echo "Error: \"$BOOKNAME\" is not a file"
	echo
	usage_function
	exit 1
fi


# Gender check
if [[ -z "$SPEACHVOICE" ]];then
	echo "Error: voicename not set"
	echo
	usage_function
	exit 1
else
	if [ -z $GENDER ];then
		if [ $GENDER == "male" || $GENDER == "MALE" ];then
			GENDER="MALE"
		elif [ $GENDER == "female" || $GENDER == "FEMALE" ];then
			GENDER="FEMALE"
		else
			echo "Error: $GENDER is not a valid gender"
			echo
			usage_function
			exit 1
		fi

	fi
fi



echo "book $BOOKNAME"
# Set output filename
if [ SSML ];then
	OUTPUTFILE=$(echo "$BOOKNAME"|sed 's/\.ssml//i')
	INPUT_TYPE='ssml'
else
	OUTPUTFILE=$(echo "$BOOKNAME"|sed 's/\.txt//i')
	INPUT_TYPE='txt'
fi
OUTPUTFILE+="`dirname "$BOOKNAME"`.mp3"
if [ OUTPUT_FILE_ASSIGNED ];then
	OUTPUTFILE=$OUTPUT_FILENAME_ASSIGNED
else
	OUTPUTFILE+=".mp3"
fi

# if [[ "$DIR" = /* ]]; then
# Starting
echo "Converting: $BOOKNAME"
echo "	Output: $OUTPUTFILE"


BOOKNAME=`readlink -f "$BOOKNAME"`

# echo "Book: $BOOKNAME"

# Generate tmp dirs
TMPDIR=`mktemp -d`
cd $TMPDIR
echo "	Temp directory: $TMPDIR"

# mkdir -p tmp
# mkdir -p tmp/bak
# mv tmp/* tmp/bak/ &> /dev/null
# $(rm tmp/*.*)
# cd tmp

echo "	Google auth file: $GOOGLE_APPLICATION_CREDENTIALS"
echo "	Voice: $SPEACHVOICE"
echo "	Gender: $GENDER"

# import credentals file
export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS


# split into 5000 max charator files, google limit per request, less lines, gives less errors
split -C $SPLITSIZE -a 4 --numeric-suffixes=0 --additional-suffix=".txt" "$BOOKNAME" SECTION

# Display section counts
SECTIONSLIST=(SECTION*.txt)
SECTIONCOUNT=`echo "${SECTIONSLIST[@]: -1}" | sed 's/SECTION//'|sed 's/\.txt//'`
echo "	File split into $SECTIONCOUNT sections"

echo -n "Converting."
# Encoding text section to audio
for FILENAME in $(ls SECTION*)
do
	# echo "Converting: $FILENAME"
	echo -n "."
	# echo "$FILENAME"

	TEXT="<speak>`cat $FILENAME | \
		sed 's/<speak>//g' |\
		sed 's/<\/speak>//g' |\
		sed 's/['\''’‚‘´\`]/’/g' |\
		sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
		sed 's/…/.../g' |\
		sed 's/[–]/-/g'  `</speak>"
	# echo $TEXT
		# remove posible inconsistent quote problems
		#TODO find a better dingle quote for I'll can't ets
		# "‚" != comma

		# double quotes: [„“‟”’"❝❞⹂〝〞〟＂]
		# single quotes" [’‚‘‛❛❜❟´\`]
		# other: /…/
# ç.
	# printf -v TEXT "%q" "`cat $FILENAME`" #remove any prob with quotes
	# TEXT="`cat $FILENAME| tr -dc '[:alnum:]\n\r'`"
	echo $TEXT > "$FILENAME-text-sent.txt" # for debuging

	# Sends text to google and returns audio
	# speaking_rate
	TRY=0
	while [ $TRY -le 2 ]; do
		
		# m,aybe change to ssml
		# https://cloud.google.com/text-to-speech/docs/ssml


		curl -s -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
		  -H "Content-Type: application/json; charset=utf-8" \
	  --data "{
		'input':{
		  '$INPUT_TYPE':'$TEXT'
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

		# problem with the sections text, usually odd char
		if [ "$?" != "0" ]; then
			echo "Failure to encode section: $FILENAME"
			echo "Content:"
			echo "    $TEXT"
		fi

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

# echo "PWD: " `pwd`

# if ! [ `ls *.mp3` ]; then
	# echo "Error: no mp3s created"
	# exit 1
# fi

# Joins audio sections to single file


if ! [ $(ffmpeg -y -loglevel 8 -f concat -safe 0 -i <(for f in ./*.mp3; do echo "file '$PWD/$f'"; done) -b:a $BITRATE -af "apad=pad_dur=2" "$OUTPUTFILE") ]; then
	echo
	echo "Success: $OUTPUTFILE"
else
	# echo "ffmpeg -y -loglevel 8 -f concat -safe 0 -i <(for f in ./*.mp3; do echo "file '$PWD/$f'"; done) -b:a $BITRATE "$OUTPUTFILE"
	echo "Error: merging sections failed"

	echo "	Command: ffmpeg -y -loglevel 8 -f concat -safe 0 -i <(for f in ./*.mp3; do echo \"file '$PWD/$f'\"; done) -b:a $BITRATE \"$OUTPUTFILE\"  "
	exit 1
fi


# Delete tmp files
# if [ $DELETETMPFILES ]; then
	# cd ..
	# rm -rf tmp
# fi

exit 0
