#!/usr/bin/perl
# Kmeans scripts as used to cluster data in
# Sorin & Pande, Biophys J. 88, 2472-2493 (2005).
# version 2.0 -- Last modified 12-23-2010 by EJS


#####	initialize variables #####
$hold = 0;
$numexp = 0;
$conv = 10;
$known_centers = 0;
$n = 100;
sub numeric {$a <=> $b}
for($i=0;$i<100;$i++){
  $mult{$i} = 1;
}


######  define I/O and open input/output files	######
$input = "\nUsage\:  Kmeans_clustering_v20.pl  [options]\n

	FLAG 	PURPOSE 			DEFAULT
	-data 	data file for clustering	MUST SPECIFY
	-k 	number of centers		MUST SPECIFY
	-name	output file prefix		MUST SPECIFY			
	-nume	number of experiments		MUST SPECIFY			
	-conv 	convergence requirement		$conv iterations
	-iter 	maximum iterations		$n iterations
	-clu	cluster center file		optional (for fitting)
	-mult   multiplier 			optional (-mult field multiplier)
 	-hold   do not move centers		OFF (for testing only)

	Note on -mult: (a) when using the -mult flag, start counting fields from 1 rather 
	than 0 as perl cannot read \"0\" in from the command line; (b) -mult can be used
	multiple times on distinct fields.

	Note on -clu: when fitting to specified clusters using the -clu flag, also set
	-iter = 1 and -conv = 1 and use -hold flag.
\n";


##### get input parameters & flags #####
if(defined(@ARGV)) {
  @options = @ARGV;
  for ($i=0; $i<=$#ARGV; $i++) {
    $flag = $ARGV[$i];
    chomp $flag;
    if($flag eq "-clu"){ $known_centers = 1; $i++; $clufile = $ARGV[$i]; next; }
    if($flag eq "-k"){ $i++; $K = $ARGV[$i]; next; }
    if($flag eq "-data"){ $i++; $data = $ARGV[$i]; next; }
    if($flag eq "-conv"){ $i++; $conv = $ARGV[$i]; next; }
    if($flag eq "-iter"){ $i++; $n = $ARGV[$i]; next; }
    if($flag eq "-name"){ $i++; $name = $ARGV[$i]; next; }
    if($flag eq "-nume"){ $i++; $numexp = $ARGV[$i]; next; }
    if($flag eq "-hold"){ $hold = 1; next; }
    if($flag eq "-mult"){ $i++; $field = $ARGV[$i] - 1; $i++; $mult{$field} = $ARGV[$i]; next; }
  }
}else{
  print "$input\n"; exit();
}


###### 	File I/O  #######
$out = "$name".".kmeans".".$K.txt";
open(OUT,">$out") or die "Can't write to $out\n";
if($known_centers == 0){ print OUT "\# initial random cluster centers K = $K\n"; 
}else{ print OUT "\# cluster centers taken from $clufile \#\n"; }
print OUT "\# maximum number of iterations = $n\n"; 
print OUT "\# number of consant iterations prior to convergence = $conv\n"; 
for($z=0;$z<=$numexp;$z++){
    $zz=$z+1;
    if($mult{$z} != 1){
	print OUT "\# field $zz being multiplied by $mult{$z}\n";
    }
}

# flush the print spooler to the OUT output file #
select OUT;
$|=1;


######  read in data file  ######
$i = 0;
open(DAT,"<$data") or die "Can't read from data file\n";
while(defined($line = <DAT>)) {  
  $i++;
  for($line) {  s/^\s+//; s/\s+$//; s/\s+/ /g; }
  @expression = split(/ /,$line);
  $numcols = scalar(@expression) - 1;

  # keep track of maximum absolute value in each dimension #
  for($exp=0;$exp<$numexp;$exp++) {
    $test[$i][$exp] = $mult{$exp} * @expression[$exp];
    $trial2 = $test[$i][$exp]*$test[$i][$exp];
    $trial = sqrt($trial2);
    if($trial > $max[$exp]) { $max[$exp]=$trial; }
  }
  $run[$i]   = @expression[$numcols - 3];
  $clone[$i] = @expression[$numcols - 2];
  $time[$i]  = @expression[$numcols - 1];   
  $proj[$i]  = @expression[$numcols];
}
close(DAT);
$numtest = $i;
print OUT "\# number of data used = $numtest\n"; 


####### read in cluster centers file or generate randomly #########
if($known_centers == 1){ 
  $i=0;
  open(CLU,"<$clufile") or die "Error: Can't read from $clufile\n";
  while(defined($line = <CLU>)) {  
    for($line) {  s/^\s+//; s/\s+$//; s/\s+/ /g; }
    @data = split(/ /,$line);
    for($exp=0;$exp<$numexp;$exp++) {
      $center[$i][$exp] = $data[$exp]; 
    }  
    $numdata[$i]==0;
    $i++;
  }
  close(CLU);
}elsif($known_centers == 0){ 
  for($i=0;$i<$K;$i++) { 
    for($exp=0;$exp<$numexp;$exp++) {
      $center[$i][$exp] = rand $max[$exp]; 
    }
  }
}else{
  print STDOUT "Error: known_centers variable not 1 or 0\n";
  exit();
}


######	   iterate n times 	######
$agree = 0;
for($num=1;$num<=$n;$num++) {
  if($agree<$conv) {
    for($j=0;$j<$K;$j++) {
      $numdata[$j]=0;
    }
    # assign initial clusters #
    for($i=1;$i<=$numtest;$i++) {
      $mindist[$i] = 1000;
      $mindist2[$i] = 1000;
      for($j=0;$j<$K;$j++) {
        $d2sum = 0;
        for($exp=0;$exp<$numexp;$exp++) {
          $dist2 = ($test[$i][$exp]-$center[$j][$exp])*($test[$i][$exp]-$center[$j][$exp]);     
          $d2sum+=$dist2;
        }
        $dist[$i][$j] = sqrt($d2sum);
        if($dist[$i][$j] < $mindist[$i]) {
    	  $mindist[$i] = $dist[$i][$j];
	  $cluster[$i] = $j;
        }
        if(($dist[$i][$j] < $mindist2[$i])&&($dist[$i][$j] > $mindist[$i])){
    	  $mindist2[$i] = $dist[$i][$j];
        }
      }
      $numdata[$cluster[$i]]++;
    }

    # now iterate over the near datum and reassign cluster centers unless -hold is used #
    if($hold == 0){
      for($j=0;$j<$K;$j++) {
        $numdata[$j] = 0;
        for($exp=0;$exp<$numexp;$exp++) { $center[$j][$exp] = 0; }
        for($i=1;$i<=$numtest;$i++) {
          if($cluster[$i] == $j) {
            $numdata[$j]++;
	    for($exp=0;$exp<$numexp;$exp++) {
  	      $center[$j][$exp]+=$test[$i][$exp];
            }
          }
        }
      }

      # if void, reassign cluster randomly #
      for($j=0;$j<$K;$j++) {
        for($exp=0;$exp<$numexp;$exp++) {
          if($numdata[$j]==0) { 
            $center[$i][$exp] = rand $max[$exp];
          }else{
      	    $center[$j][$exp]/=$numdata[$j];
          }
        }
      }

      # bookkeeping: look for convergence #
      $agreenum = 0;
      for($j=0;$j<$K;$j++) {
        if($numdata[$j] == $numold[$j]) { $agreenum++; }
        if($agreenum == $K) { $agree++; }
        $iter++;
        $numold[$j] = $numdata[$j];
      }
    }

  # end iterations if converged #
  }else{
    $numc = $num - 10;
    print OUT "\# convergence occurred in $numc iterations\n";
    last;
  }
}  

# print total number of resulting clusters #
$numfinalclusters = 0;
for($j=0;$j<$K;$j++) {
  if(($numdata[$j] > 0)||($hold)){
	$numfinalclusters++;
  }	
}
print OUT "\# number of resulting clusters = $numfinalclusters\n"; 

# print the centers #
print OUT "\#  group  pop\tcenters\n";
for($j=0;$j<$K;$j++) {
  if(($numdata[$j] > 0)||($hold)){
    printf OUT "%6d %6d\t",$j,$numdata[$j];
    for($exp=0;$exp<$numexp;$exp++) {
      @cent[$exp]=$center[$j][$exp];
      printf OUT "%8.3f\t",$center[$j][$exp];
    }
    @sorted = sort numeric @cent;
    print OUT "\n";
  }
}

# print out result of all n iterations #
printf OUT "\n\# Class\tdist(1)\tdist(2)\t<Delta(dist)>\n";
$del=0;
$delmin1=0;
$delmin2=0;
for($i=1;$i<=$numtest;$i++) {
  $del=($mindist2[$i]-$mindist[$i]);
  $del2 = (($mindist2[$i]*$mindist2[$i])-($mindist[$i]*$mindist[$i]));
  $deldiff+=$del2;

  $delmin1+=($mindist[$i]*$mindist[$i]);
  $delmin2+=($mindist2[$i]*$mindist2[$i]);
  printf OUT "%6d %8.2f %8.2f %8.2f ",$cluster[$i],$mindist[$i],$mindist2[$i],$del;
  for($cujo=0;$cujo<$numexp;$cujo++){ 
    printf OUT " %12.3f ",$test[$i][$cujo];  
  } 
  printf OUT "\t$run[$i]\t$clone[$i]\t$time[$i]\t$proj[$i]\n";
}
$delmin1/=$numtest;
$del1 = sqrt($delmin1);
$delmin2/=$numtest;
$del2 = sqrt($delmin2);
$deldiff/=$numtest;
$del3 = sqrt($deldiff);

printf OUT "\n\nMSD1=%12.6f\nMSD2=%12.6f\nMSDdiff=%12.6f\n",$del1,$del2,$del3;
close (OUT);


####################### I/O file format ############################
#
# 1. Input data file:
#
#    0.33  -0.17   0.04  -0.07	run	clone	time	proj
#   -0.64  -0.38  -0.32  -0.29	run     clone   time    proj
#   -0.23   0.19  -0.36   0.14  (use these if you want to!)
#   -0.69  -0.89  -0.74  -0.56
#    0.04   0.01  -0.81   0.00
#    0.11   0.32   0.03   0.32
#   -0.47   1.00  -0.51  -0.25
#
#   columns are individual timepoints 
#   rows are specific events (to be clustered)
#
#
# 2. Output Kmeans.$K.class file
#
#   .       .      
#   .       .        
#   8       1        
#   9       1        
#   10      1        
#   11      1        
#   12      1          
#   13      1         
#   .       .        
#   .       .         
#
#   order: test gene index, predicted class
#
#######################################################################
