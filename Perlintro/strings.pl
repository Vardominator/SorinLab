use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;



my $long_string = "Random Long String";

say "Length of string: ", length $long_string;


printf("Long is at %d \n", index $long_string, "Long");

printf("Long g is at %d \n", rindex $long_string, "g");


#concatenate
$long_string = $long_string . " isn\'t that long";


#starting index and total number of characters to receive 
say "Index 7 through 10 ", substr $long_string, 7, 4;


my $animal = "animals";
printf("Last character is %s\n", chop $animal);


my $no_newline = "No newline\n";
chomp $no_newline;


printf("Uppercase : %s \n", uc $long_string);
printf("Lowercase : %s \n", lc $long_string);
printf("1st Uppercase : %s \n", ucfirst $long_string);



#replace list of characters on the left with list of chars on right
$long_string =~ s/ /, /g;  
#Take all of the spaces and replace them with a comma and a space

say $long_string;


# repeat
my $two_times = "What I said is " x 2;


# array
my @abcs = ('a' .. 'z');


# combine values in an array and find the separation
print join(", ", @abcs), "\n";
# separate all the different characters with a comma and a space


my $letter = 'c';
say "Next letter ", ++$letter;




















