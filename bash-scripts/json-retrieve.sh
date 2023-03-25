#!/usr/bin/env bash

present=$(pwd)
mkdir "temp"
cd temp || exit
git clone https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes.git
git clone https://github.com/russ666/all-countries-and-cities-json.git
cd ISO-3166-Countries-with-Regional-Codes/slim-3 || exit
cp slim-3.json "$present"
cd "$present/temp//all-countries-and-cities-json" || exit
cp countries.json "$present"
cd "$present" || exit
mv slim-3.json data/iso-3166-code.json
mv countries.json data/cities.json
rm -rf temp
