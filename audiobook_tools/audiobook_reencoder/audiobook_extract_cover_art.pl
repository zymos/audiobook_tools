#!/usr/bin/perl 
#
use File::Find;
# Config

$TEST = 0;

$dirname = $ARGV[0];

if($dirname eq ""){
  print "the first arg is the directory\n";
  exit;
}


print "starting processes....\n";

sub the_operation {
	my $file = $_;
	if( not( $file eq '.' || $file eq '..') && ( $file =~ /\.[mM][pP]3/ ) ) {
		# $file2 = $file;

		my @files1 = glob( "*.[jJ][pP][gG]" );
		my @files2 = glob(  "*.[pP][nN][gG]" );

		if( !( @files1 || @files2 ) && $file =~ /\.m[p4][b3]$/ ){
			print "\n# Extracting cover art -> cover.jpg\n";
			$command = "ffmpeg -nostats -hide_banner -loglevel panic -i \"$file\" \"cover.jpg\"";
			if( ! $TEST ){
				$out = `$command`;
			}else{
				print ">>Test/Executing: $command\n";
			}

		}else{
			print ".";
		}
	}
}


print "######################################################\n"
print "# Extracting cover art from mp3\n";
print "# Directory: $dirname\n";
print "#\n";

find(\&the_operation, $dirname);

print "\ndone...\n\n";

