 #!/bin/bash
 set -B
 for i in {1..200}; do
 	curl https://lcgcdn.s3.amazonaws.com/mc/MC12en_$i.jpg --output MC12en_$i.jpg
 done

 for i in {1..200}; do
 	for x in "a" "b" "c" "d"
 	do
 		# echo "$i - $x"
 		curl https://lcgcdn.s3.amazonaws.com/mc/MC12en_$i$x.jpg --output MC12en_$i$x.jpg
 	done
 done

 for i in {1..200}; do
 	for x in "A" "B" "C" "D"
 	do
 		# echo "$i - $x"
 		curl https://lcgcdn.s3.amazonaws.com/mc/MC12en_$i$x.jpg --output MC12en_$i$x.jpg
 	done
 done