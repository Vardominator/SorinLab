use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;


my @primes = (2,3,5,7,11,13,17);

my @my_info = ("Vardo", "123 Main Street", 40, 6.25);


$my_info[4] = "Barsegyan";


for my $info (@my_info){
	say $info;
}

foreach my $num (@primes){
	say $num;
}

for (@my_info){
	say $_;
}


my @my_name = @my_info[0, 4];
say @my_name;


my $items = scalar @my_info;

say $items;


my ($f_name, $address, $how_old, $height, $l_name) = @my_info;


say "$f_name $l_name";


# remove the last item
say "Popped Value ", pop @primes;

# add something to the end
say "Pushed Value ", push @primes, 17;

# move everything to the left
say "First item ", shift @primes;

for(@primes){say $_;}

# add something to the front
say "Unshifted item ", unshift @primes, 2;

for(@primes){say $_;}

# concatenate items with a comma
print join(", ", @primes), "\n";

# remove items at indices
say "Remove Index 0 - 2 ", splice @primes, 0, 3;
print join(", ", @primes), "\n";


print join " ", ('list', 'of', 'words', "\n");


my $customers = "Sue Sally Paul";

# split an array
my @cust_array = split / /, $customers;
print join (", ", @cust_array), "\n";


# reverse and sort
@cust_array = reverse @cust_array;
@cust_array = sort @cust_array;
@cust_array = reverse sort @cust_array;


# filter a list according to an expression
my @number_array = (1,2,3,4,5,6,7,8);
my @odds_array = grep {$_ % 2} @number_array;
print join(", ", @odds_array), "\n";


# perform a function on every item in the array
my @dbl_array = map {$_ * 2} @number_array;
print join(", ", @dbl_array), "\n";



















