# m4bsplit 
The purpose of this software is to split m4b file's chapters into seperate files of MP3, M4A, M4B, flac and ogg formats through a basic bash script frontend to FFMPEG. This script is based on AAXtoMP3 code.

## Requirements
* bash 4.3.42 or later tested
* ffmpeg version 2.8.3 or later
* libmp3lame (came from lame package on Arch, not sure where else this is stored)
* grep Some OS distributions do not have it installed.
* sed Some OS versions will need to install gnu sed.
* mp4art used to add cover art to m4a and m4b files. Optional

## Usage(s)
```
Usage: m4bsplit [--flac] [--aac] [--opus ] [--single] [--chaptered]
[-e:mp3] [--no-clobber]
[--target_dir <PATH>] [--complete_dir <PATH>] [--validate]
{FILES}
```

## Options
* **-f** or **--flac**   Flac Encoding and Produces a single file.
* **-o** or **--opus**   Ogg/Opus Encoding defaults to multiple file output by chapter. The extension is .ogg
* **-a** or **--aac**    AAC Encoding and produce a m4a single files output.
* **-n** or **--no-clobber** If set and the target directory already exists, AAXtoMP3 will exit without overwriting anything.
* **-t** or **--target_dir &lt;PATH&gt;** change the default output location to the named &lt;PATH&gt;. Note the default location is ./Audiobook of the directory to which each AAX file resides.
* **-C** or **--complete_dir &lt;PATH&gt;** a directory to place aax files after they have been decoded successfully. Note make a back up of your aax files prior to using this option. Just in case something goes wrong.
* **-V** or **--validate** Perform 2 validation tests on the supplied aax files. This is more extensive than the normal validation as we attempt to transcode the aax file to a null file.  This can take a long period of time. However it is useful when inspecting a large set of aax files prior to transcoding. As download errors are common with Audible servers.
* **-e:mp3**         Identical to defaults.
* **-e:m4a**         Create a m4a audio file. This is identical to --aac
* **-e:m4b**         Create a m4b audio file. This is the book version of the m4a format.
* **-s** or **--single**    Output a single file for the entire book. If you only want a single ogg file for instance.
* **-c** or **--chaptered** Output a single file per chapter. The `--chaptered` will only work if it follows the `--aac -e:m4a -e:m4b` options.

### MP3 Encoding
* This is the **default** encoding
* Produces 1 or more mp3 files for the AAX title.
* The default mode is **chaptered**
* If you want a mp3 file per chapter do not use the -single option. 
* A m3u playlist file will also be created in this instance in the case of **default** chaptered output.

### Ogg/Opus Encoding
* Can be done by using the **-o** or **--opus** command line switches
* The default mode is **chaptered**
* Opus coded files are stored in the ogg container format for better compatibility.

### AAC Encoding
* Can be done by using the **-a** or **--aac** command line switches
* The default mode is **single**
* Designed to be the successor of the MP3 format
* Generally achieves better sound quality than MP3 at the same bit rate.
* This will only produce 1 audio file as output.

### FLAC Encoding
* Can be done by using the **-f** or **--flac** command line switches
* The default mode is **single**
* FLAC is an open format with royalty-free licensing
* Note: There is an bug with the ffmpeg software that prevents the splitting of flac files. Chaptered output of flac files will fail.

### M4A and M4B Containers
* These containers were created by Apple Inc. They were meant to be the successor to mp3.
* M4A is a container that is meant to hold music and is typically of a higher bitrate.
* M4B is a container that is meant to hold audiobooks and is typically has bitrates of 64k and 32k.
* Both formats are chaptered
* Both support coverart internal
* The default mode is **single**

### Defaults
* Default out put directory is the base directory of each file listed. Plus the genre, Artist and Title of the Audio Book.
* The default codec is mp3
* The default output is by chapter.

### Installing Dependencies.
#### FFMPEG,FFPROBE
__Ubuntu, Linux Mint, Debian__
```
sudo apt-get update
sudo apt-get install ffmpeg libav-tools x264 x265 bc
```

__Fedora__

Fedora users need to enable the rpm fusion repository to install ffmpeg. Version 22 and upwards are currently supported. The following command works independent of your current version:
```
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
Afterwards use the package manager to install ffmpeg:
```
sudo dnf install ffmpeg
```

__RHEL or compatible like CentOS__

RHEL version 6 and 7 are currently able to use rpm fusion.
In order to use rpm fusion you have to enable EPEL, see http://fedoraproject.org/wiki/EPEL

Add the rpm fusion repositories in version 6
```
sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-6.noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-6.noarch.rpm
```
or version 7:
```
sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm
```
then install ffmpeg:
```
sudo yum install ffmpeg
```

__MacOS__
```
brew install ffmpeg
brew install gnu-sed
brew install grep
```

#### mp4art
_Note: This is an optional dependency._

__Ubuntu, Linux Mint, Debian__
```
sudo apt-get update
sudo apt-get install mp4v2-utils
```
__CentOS, RHEL & Fedora__
```
# CentOS/RHEL and Fedora users make sure that you have enabled atrpms repository in system. Let’s begin installing FFmpeg as per your operating system.
yum install mp4v2-utils

```
__MacOS__
```
brew install mp4v2
```

## License
This is based almost entirely from [AAXtoMP3](https://github.com/KrumpetPirate/AAXtoMP3) by KrumpetPirate
L, do whatever you like with this script. Ultimately it's just a front-end for ffmpeg after all.

