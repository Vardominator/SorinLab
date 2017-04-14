use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;

print "Hello mother fuckers\n";


my $name = "Vardominator";

my ($age, $street) = (40, "123 Main Street");

my $my_info = "$name lives on $street\n";

print $name;

print $my_info;

my $bunch_of_info = <<"END";
This is a
bunch of information
on multiple lines
END

say $bunch_of_info;


my $big_int = 12334039475098;


printf("%u \n", $big_int + 1);


my $big_float = .1000000000001;

printf("%.16f \n", $big_float + .1000000000001);


my $first = 1;
my $second = 2;

#Switch values
($first, $second) = ($second, $first);


say "5/4 = ", 5/4;
say "5%4 = ", 5%4;
say "5**4", 5**4;


say "exp 1 = ", exp 1;
say "hex 10 = ", hex 10;
say "oct 10 = ", oct 10;
say "int 6.45", int(6.45);
say "log 2 = ", log 2;
say "random between 0 - 10 = ", int(rand 11);
say "sqrt 9 = ", sqrt 9;




my $rand_num = 5;
$rand_num += 1;

say "Number Incremented ", $rand_num;


say "6++ = ", $rand_num++;
say "++6 = ", ++$rand_num;
say "6-- = ", $rand_num--;
say "--6 = ", --$rand_num;

say "3 + 2 * 5 = ", 3 + 2 * 5;
say "(3 + 2) * 5 = ", (3 + 2) * 5;






































