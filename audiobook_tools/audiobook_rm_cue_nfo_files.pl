#!/usr/bin/perl 
#
use File::Find;

#################################################
# Deletes all cue and nfo files in a directory recusivly
#


#################################################
# Config

$DEBUG = 1;


#################################################
# Code
#


# Input arguments
$dirname = $ARGV[0];

if($dirname eq ""){
  print "the first arg is the directory\n";
  exit;
}



sub the_operation {
	my $file = $_;
	if( not( $file eq '.' || $file eq '..') && ( $file =~ /\.cue/ || $file =~ /\.nfo/ ) ) {
		# $file2 = $file;
		if( $use_trash_rm ) { # Use trash-rm instead of rm
			$command = "trash-put \"$file\"";
		}else{
			$command = "rm -f \"$file\"";
		}
		$out .= `$command`;
		print "Deleting: $file\n";
		if($DEBUG){ print "->$command\n"; }
	}
}


print "######################################################\n";
print "# Deleting cue and nfo files\n";
print "# Directory: $dirname\n";
print "#\n";

# Use trash-rm instead of rm
if( `which trash-put` ) { 	
	$use_trash_rm = 1;
	print "# Using trash_cli instead of rm\n";
}else{
	$use_trash_rm = 0;
}


find(\&the_operation, $dirname);

print "\ndone...\n\n";

