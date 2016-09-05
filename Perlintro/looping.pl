use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.16;


#for
for(my $i = 0; $i < 10; $i++)
{

	say $i;

}


#while
my $j = 1;
while($j < 10)
{

	if($j % 2 == 0)
	{
	
		$j++;
		next;	#continue
	
	}
	
	if($j == 7)
	{
	
		last;	#break
	
	}
	
	say $j;
	$j++;

}


# do while
my $lucky_num = 7;
my $guess;

do
{

	say "Guess a number between 1 and 10";
	
	$guess = <STDIN>;


}while $guess != $lucky_num;



#switch-case
my $age_old = 18;

given($age_old){

	when($_ > 16){
		say "Drive";
		continue;
	}
	
	when($_ > 17){
		say "Go vote!";
	}
	
	default{
		say "Nothing special";
	}
	
}




















