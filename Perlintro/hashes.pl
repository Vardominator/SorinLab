use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;


# not a dollar sign
my %employees = (

	"Sue" => 35,
	"Paul" => 43,
	"Sam" => 39

);


printf("Sue is %d \n", $employees{Sue});


# add new keys to the hash
$employees{Frank} = 44;


while(my ($k, $v) = each %employees){

	print "$k $v\n";

}


# slice data from a hash
my @ages = @employees{"Sue", "Sam"};
print join (', ', @ages), "\n";


# convert hash into array
my @hash_array = %employees;


# delete key as well as value
delete $employees{'frank'};

while(my($k, $v) = each %employees){

	print "$k $v\n";

}



say ((exists $employees{'Sam'}) ? "Same is here" : "No same");


for my $key (keys %employees){

	if($employees{$key} == 35){
	
		say "Hi Sue";
	
	}

}


for my $value (values %employees){

	say $value;

}























