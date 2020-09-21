#!/bin/bash

PYT="/usr/bin/python3"
threed="100"
path_url="contrib/urls"
path_dom="contrib/domains"
out_u="check/urls"
out_d="check/domains"
marker="ограничен"
dir="check/"
mail="chulkov@netonline.ru"

echo "extfilter_maker.pl"
./extfilter_maker.pl
sleep 3
echo "Check URLs"
$PYT rkn_check.py -t $threed -f $path_url -m $marker -o $out_u
sleep 3
echo "Check DOMAINs"
$PYT rkn_check.py -t $threed -f $path_dom -m $marker -o $out_d
echo "Проверено"
$PYT send_to_mail.py -e $mail -f $dir
sleep 5


