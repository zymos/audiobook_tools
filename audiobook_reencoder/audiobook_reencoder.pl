#!/usr/bin/perl

############################################################################
#   			Audiobook Encoder
#
#	Description: ReEncodes a mp3 into a optimize audiobook mp3 file
#	Specs: 	bitrate: 32kbps; 
#			sample-rate: 22050Hz;
#			bandwidth: 7kHz
#			ID3v2 content type: "Audiobook"
#			Volume nomalized: Yes
#			Backup directory: in config section
#	Author:	ZyMOS
#	Date: 	17 June 2016 -
#	License: GPLv2
#	Requirments:
#		LAME MP3 Encoder (http://lame.sourceforge.net/)
#		MP3Gain (http://mp3gain.sourceforge.net/)
#		id3v2 (http://id3v2.sourceforge.net/)
#		avconv ()
#
############################################################################




################################
# Config
#

$TEST = 0;
$LOG_DIR = "/tmp/";
$BACKUP_DIR = "/tmp/original_audio_files";

$NORMALIZATION = 1;
$DELETE_ORIGINAL = 1;
$USE_MP3GAIN_FOR_NORMALIZATION = 1;
$ADD_ID3_AUDIOBOOK_TAG = 1;

$DELETE_CUE_FILE = 1;





#################################
#  Code
#

use File::Find;
# use File::Path;
use File::Path qw(make_path);
# use Cwd;
use Cwd 'abs_path';


# Check input must inckude dir
$dirname = $ARGV[0];
if($dirname eq "" || !(-d $dirname) ){
  print "Error: the first arg is the directory\n";
  print "Usage: audiobook_reencoder.pl [DIRECTORY]\n";
  exit 1;
}




sub m4btomp3 {
	my $file = $_;
	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	
	my $file2 = $file;
	$file2 =~ s/[Mm]4[AaBb]$/.tmp-for-m4b.mp3/;

	print "# Convert m4b/m4a to mp3...\n";
	print "#  [$file] to [$file2]\n";
	
	$command = "avconv -loglevel \"fatal\" -i \"$file\" -c:v copy \"$file2\""; # c:v copy copies cover art
	if(! $TEST ){
		$out = `$command`;
	}else{
		print ">>Executing: $command\n";
	}
	return($file2);
}




sub backup_files{
	my $file = $_;
	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	

	if($DELETE_ORIGINAL){ # Delete the origional files after encoding
		print "# Deleting original file...\n";
		$command = "/bin/rm \"$file\"";
		if(! $TEST ){
			#sleep before delete incase you made a 
			# terrible mistake and want to Ctrl-c
			sleep(3); 
			$out = `$command`; 
		}else{
			print ">>Executing: $command\n";
		}
	}elsif( -e $BACKUP_DIR . "/" . $file ){ #Backup original file, if file already exists, move to 
		 # backup dir as dup filename
		print "# Moving original file to backup directory...\n";
		$dup = $BACKUP_DIR . "/" . $file . "-dup.mp3";
		$command = "mv \"$file\" \"$dup\"";
		if(! $TEST ){
			$out = `$command`; 
		}else{
			print ">>Executing: $command\n";
		}
	}else{ # Backup origional file, move to backup dir
		print "# Moving original file to backup directory...\n";
		$command = "mv \"$file\" \"$BACKUP_DIR\"";
		if(! $TEST ){
			$out = `$command`;
		}else{
			print ">>Executing: $command\n";
		}
	}

	if($DELETE_CUE_FILE){
		my $cue_file =~ s/\.mp3$/.cue/;
		if( -e $cue_file )
		$command = "/bin/rm \"$file\"";
		if(! $TEST ){
			#sleep before delete incase you made a 
			# terrible mistake and want to Ctrl-c
			$out = `$command`; 
		}else{
			print ">>Executing(rm cue file): $command\n";
		}
	}
}



# Encode the files
sub the_operation {
	my $file = $_;
	my $file2 = '';

	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	
	# print "$top_dir\n";
	
	# Skip directories
	if( $file eq '.' || $file eq '..' || -d $file ){ #skip dirs
		#	print "skip\n";
		return;
	}

	#skip non-audiobooks ! *.mp3 or *.m4b
	if( !( $file =~ /\.mp3/i || $file =~ /\.m4b/i  || $file =~ /\.m4a/i ) ){
		return;
	}

	
	# Print a header for encoding
	print "\n\n\n##################################################################\n";
	print "##################################################################\n";
	print "# Encoding: [$file] \n#      in [$top_dir]\n";
	print "# Processing [$count] of [$total_file_count]\n";
	print "#\n";


	# preprocess M4B files
	my $is_m4b=0;
	if( $file =~ /\.m4b$/i || $file =~ /\.m4a$/i ){
		$file2 = &m4btomp3($file);
		&backup_files($file);
		$file = $file2;
		$is_m4b=1;
	}

	# dont encode if its definatly already encoded
	if($file =~ /-32k-32k\.mp3$/){ # Skip encoding
		print "# Skipping Encoding: [$file]\n";
		print "# file is definitly already encoded...\n";
		print "#\n";
		$count += 1;
	}elsif( not( $file eq '.' || $file eq '..' ) && $file =~ /\.mp3$/i && $top_dir ne "original") { #make sure its an mp3

		# Create new file name
		$file2 = $file;
		if( $is_m4b ){
			$file2 =~ s/\.[Mm]4[AaBb]\.tmp-for-m4b.mp3$/-32k.mp3/;
		}else{
			$file2 =~ s/\.[Mm][Pp]3$/-32k.mp3/;
		}
	
		# print "# Encoding: [$file] \n    in [$top_dir]\n";
		# print "# Processing [$count] of [$total_file_count]\n";
		$count += 1;
		
		# The encoding processes, (lame + id3 + mp3gain + del orginal)
		if(!$NORMALIZATION){
			$lame_normalization_arguments = "--noreplaygain";
		}elsif(!$USE_MP3GAIN_FOR_NORMALIZATION){
			$lame_normalization_arguments = "--replaygain-accurate";
		}else{
			$lame_normalization_arguments = "--noreplaygain";
		}
		print "# Starting Lame...\n";
		$lame_command = "lame --quite --resample 22050 --cbr -b 32 $lame_normalization_arguments \"$file\" \"$file2\"";
		if(! $TEST ){
			$out = `$lame_command`;
		}else{
			print ">>Executing: $lame_command\n";
		}

		if($? && !$TEST){ # lame encode failed
			print "# ERROR encoding: $file \n";
			print FILE "Fail: $file\n";
			print "# Deleting newly created, failed file\n";
			$out = `rm -f "$file2"`;
			print "EXITING (1)\n";
			exit 1;
		}else{ #lame sucsseded
			print FILE "Good: $file2\n";
			if($ADD_ID3_AUDIOBOOK_TAG){
				print "# Applying ID3 tag, \"Audiobook\" genre...\n";
				$command = "id3v2 --TCON \"Audiobook\" \"$file2\"";
				if(! $TEST ){
					$out = `$command`; # ID3 tag content->"Audiobook"
				}else{
					print ">>Executing: $command\n";
				}
			}

			if($USE_MP3GAIN_FOR_NORMALIZATION && $NORMALIZATION){
				print "# Applying volume normilization...\n";
				$command = "mp3gain \"$file2\" > /dev/null 2>&1 &";	
				# replay gain
				# runs oput of perl as a seperate parrallel proccess
				if(! $TEST ){
					$out = system($command); # ID3 tag content->"Audiobook"
				}else{
					print ">>Executing: $command\n";
				}
			}
			&backup_files($file);
		}
		print "# Encoding complete\n#\n";
	}
}


##############################
# counts total files
sub the_count {
	my $file = $_;

	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	

	if( not( $file eq '.' || $file eq '..' || -d $file ) && $top_dir ne "original") { 
		if( $file =~ /\.mp3$/ || $file =~ /\.m4b$/){
			#make sure its an mp3
			$total_file_count += 1;
		}
	}
}



print "\n\n\n#########################################################################\n";
print "#########################################################################\n";
print "Starting processes...\n";

# create dir for origonals
# $orig_dir = $dirname . "/original";
# mkdir($orig_dir);
# $orig_dir = abs_path($orig_dir);

# displaying settings
print "Settings:\n";
print "  Encoding directory: $dirname\n";
print "  Log directory: $LOG_DIR\n";
print "  Backup directory: $BACKUP_DIR\n";
print "  Normalization: $NORMALIZATION\n";
print "  Delete original: $DELETE_ORIGINAL\n";
print "  Use MP3Gain for normalization: $USE_MP3GAIN_FOR_NORMALIZATION\n";
if($TEST){
	print "  ***Test mode enabled***\n";
}

# Check if programs are required
if($USE_MP3GAIN_FOR_NORMALIZATION){
	`mp3gain -v` || die "Error: 'mp3gain' not installed"
}
`avconv -version` || die "Error: 'avconv' not installed";
`lame --version` || die "Error: 'mp3lame' not installed";

if($ADD_ID3_AUDIOBOOK_TAG){
	`id3v2 -v` || die "Error: 'id3v2' not installed";
}

# create backup dir
if($DELETE_ORIGINAL){
	$BACKUP_DIR = abs_path($BACKUP_DIR);
	$BACKUP_DIR = $BACKUP_DIR . "/" . $time_string; #global var for the backup_dir
	print "Create backup directory:\n";
	print "   [$BACKUP_DIR]\n";
	make_path($BACKUP_DIR); #create the backup dir
}




# create log
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year += 1900;
$mon += 1;
$time_string = "$year-$mon-$mday--$hour-$min";
$log_file = "$LOG_DIR/audiobook_encode-$time_string.log";
print "Creating log file:\n";
print "   [$log_file]\n";
open FILE, ">>", "$log_file" or die "Log file creation failed: $!";
print FILE "Started encoding directory: $dirname\n";



# count the files
$count = 1;
$total_file_count = 0;
find(\&the_count, $dirname);
print "Counting files to encode: ";
print " $total_file_count counted...\n";


# process each file
print "Starting Encoding...\n";
find(\&the_operation, $dirname);


# close log
close FILE;
print "\n\n\nEncoding done...\n\n";
print "exit(0)\n";

exit 0;
