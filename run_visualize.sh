#!/bin/sh

for file in reduced*
do
    for hashtag in '#코로나바이러스' '#コロナウイルス' '#冠状病毒' '#covid2019' '#covid-2019' '#covid19' '#covid-19' '#coronavirus' '#corona' '#virus' '#flu' '#sick' '#cough' '#sneeze' '#hospital' '#nurse' '#doctor'  
    do
        nohup ./src/visualize.py --input_path="$file" --key=$hashtag > visualize_check/"$file"."$hashtag" &
    done
done



