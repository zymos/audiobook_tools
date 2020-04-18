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
#	Date: 	17 June 2016 - 2019
#	License: GPLv2
#	Requirments:
#		LAME MP3 Encoder (http://lame.sourceforge.net/)
#		MP3Gain (http://mp3gain.sourceforge.net/)
#		id3v2 (http://id3v2.sourceforge.net/)
#		ffmpeg ()
#
############################################################################




################################
# Config
#

$TEST = 0;
$LOG_DIR = "/home/zymos/tmp/";
$BACKUP_DIR = "/home/zymos/tmp/original_audio_files";

$NORMALIZATION = 1;
$DELETE_ORIGINAL = 1;
$USE_MP3GAIN_FOR_NORMALIZATION = 1;
$EXTRACT_COVER_ART = 1;


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
if($dirname eq ""){
  print "the first arg is the directory\n";
  exit;
}




sub m4btomp3 {
	my $file = $_;
	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	
	$file2 = $file;
	$file2 =~ s/m4b$/mp3/;

	print "# Convert m4b to mp3...\n";
	print "#  [$file] to [$file2]\n";
	
	$command = "ffmpeg -nostats -hide_banner -loglevel panic -i \"$file\" -c:v copy \"$file2\""; # c:v copy copies cover art
	if(! $TEST ){
		$out = `$command`;
	}else{
		print ">>Test/Executing: $command\n";
	}
	return($file2);
}




sub backup_files{
	my $file = $_[0];
	# Grab top directory of file
	my $top_dir = $File::Find::dir; 
	$top_dir =~ s/.*\///; 	

	if($DELETE_ORIGINAL){ # Delete the origional files after encoding
			$command = "/bin/rm \"$file\"";
			if(! $TEST ){
				#sleep before delete incase you made a 
				# terible mistake and want to Ctrl-c
				print "# Deleting original file...(Ctrl-C to cancel)...\n";
				sleep(3); 
				$out = `$command`; # ID3 tag content->"Audiobook"
			}else{
				print ">>Test/Executing DELETE: $command\n";
			}
		}elsif( -e $BACKUP_DIR . "/" . $file ){ #Backup original file, if file already exists, move to 
			 # backup dir as dup filename
			print "# Moving original file to backup directory...\n";
			$dup = $BACKUP_DIR . "/" . $file . "-dup.mp3";
			$command = "mv \"$file\" \"$dup\"";
			if(! $TEST ){
				$out = `$command`; # ID3 tag content->"Audiobook"
			}else{
				print ">>Test/Executing: $command\n";
			}
		}else{ # Backup origional file, move to backup dir
			print "# Moving original file to backup directory...\n";
			$command = "mv \"$file\" \"$BACKUP_DIR\"";
			if(! $TEST ){
				$out = `$command`; # ID3 tag content->"Audiobook"
			}else{
				print ">>Test/Executing: $command\n";
			}
	}
	return;
}



# Encode the files
sub the_operation {
	my $file = $_;
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
	if( !( $file =~ /\.mp3/i || $file =~ /.m4b/i ) ){
		return;
	}

	
	# Print a header for encoding
	print "\n\n\n##################################################################\n";
	print "##################################################################\n";
	print "# Encoding: [$file] \n#      in [$top_dir]\n";
	print "# Processing [$count] of [$total_file_count]\n";
	print "#\n";

	# Extract cover art to cover.jpg if DNE
	# print "CWD Dir: " . abs_path() . "\n";
	# $path_name = abs_path() . "/*.[jJ][pP][gG]";
	# print "PATH : $path_name";
	my @files1 = glob( "*.[jJ][pP][gG]" );
	my @files2 = glob(  "*.[pP][nN][gG]" );

	# print "Files :";
	# foreach ( @files ){
		# print "X: $_\n";
	# }
	if( !( @files1 || @files2 ) && $file =~ /\.m[p4][b3]$/ && $EXTRACT_COVER_ART ){
		print "# Extracting cover art -> cover.jpg\n";
		$command = "ffmpeg -nostats -hide_banner -loglevel panic -i \"$file\" \"cover.jpg\"";
		if( ! $TEST ){
			$out = `$command`;
		}else{
			print ">>Test/Executing: $command\n";
		}

	}else{
		print "# Cover art exists\n";
	}



	if( not( $file eq '.' || $file eq '..' ) && $file =~ /\.m4b$/ ){

		$file2 = &m4btomp3($file);
		&backup_files($file);
		$file = $file2;
	}

	# dont encode if it's already encoded
	if($file =~ /-32k\.mp3$/){ # Skip encoding
		print "# Skipping Encoding: [$file]\n";
		print "# file is already encoded...\n";
		print "#\n";
		$count += 1;
	}elsif( not( $file eq '.' || $file eq '..' ) && $file =~ /\.mp3$/ && $top_dir ne "original") { #make sure its an mp3

		# Create new file name
		$file2 = $file;
		$file2 =~ s/\.mp3$/-32k.mp3/;
	
		# print "# Encoding: [$file] \n    in [$top_dir]\n";
		# print "# Processing [$count] of [$total_file_count]\n";
		$count += 1;
		
		# The encoding processes, (lame + id3 + mp3gain + del orginal)
		if(1){ #legacy crap
			if(!$NORMALIZATION){
				$lame_normalization_arguments = "--noreplaygain";
			}elsif(!$USE_MP3GAIN_FOR_NORMALIZATION){
				$lame_normalization_arguments = "--replaygain-accurate";
			}else{
				$lame_normalization_arguments = "--noreplaygain";
			}
			print "# Starting Lame...\n";
			$lame_command = "lame --resample 22050 --cbr -b 32 $lame_normalization_arguments \"$file\" \"$file2\"";
			if(! $TEST ){
				$out = `$lame_command`;
			}else{
				print ">>Test/Executing: $lame_command\n";
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
				print "# Applying ID3 tag, \"Audiobook\" genre...\n";
				$command = "id3v2 --TCON \"Audiobook\" \"$file2\"";
				if(! $TEST ){
					$out = `$command`; # ID3 tag content->"Audiobook"
				}else{
					print ">>Test/Executing: $command\n";
				}

				if($USE_MP3GAIN_FOR_NORMALIZATION && $NORMALIZATION){
					print "# Applying volume normilization...\n";
					$command = "mp3gain \"$file2\" > /dev/null 2>&1 &";	
					# replay gain
					# runs oput of perl as a seperate parrallel proccess
					if(! $TEST ){
						$out = system($command); # ID3 tag content->"Audiobook"
					}else{
						print ">>Test/Executing: $command\n";
					}
				}
				backup_files("$file");
			}
			print "# Encoding complete\n#\n";
		}
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
