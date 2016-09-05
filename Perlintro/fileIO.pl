use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;



my $emp_file = 'fileIOdata.txt';

# '<': opening the file for reading only
open my $fh, '<', $emp_file
	or die "Can't Open File: $_";
	
	
while(my $info = <$fh>){

	chomp($info);
	
	
	my ($emp_name, $job, $id) = split /:/,
	$info;
	
	print "$emp_name is a $job and has the id $id \n";

}


close $fh or die "Coudn't close file: $_";



#putting data at the end of the file; '>>': append
open ($fh, '>>', $emp_file)
	or die "Can't open file: $_";
	
print $fh "BigSexy:Stripper\n";
close $fh or die "Couldn't close file: $_";



open $fh, '+<', $emp_file
	or die "Cant' Open File: $_";
	
seek $fh, 0, 0;

print $fh "Phil:Salesman:123\n";
close $fh or die "Couldn't close file: $_";








