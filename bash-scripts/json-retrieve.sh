#!/usr/bin/env bash

present=$(pwd)
rm -rf data temp
mkdir "temp"
mkdir "data"
cd temp || exit
git clone https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes.git
cd ISO-3166-Countries-with-Regional-Codes/slim-3 || exit
cp slim-3.json "$present"
cd "$present" || exit
mv slim-3.json data/iso-3166-code.json
rm -rf temp
