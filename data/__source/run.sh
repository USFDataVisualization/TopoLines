#!/bin/bash

. venv/bin/activate

mkdir ../eeg
python process.py -ds eeg -df chan01 > ../eeg/chan01.json
python process.py -ds eeg -df chan07 > ../eeg/chan07.json
python process.py -ds eeg -df chan14 > ../eeg/chan14.json
python process.py -ds eeg -df chan21 > ../eeg/chan21.json

mkdir ../climate
python process.py -ds climate -df t14-15 > ../climate/t14-15.json
python process.py -ds climate -df t15-16 > ../climate/t15-16.json
python process.py -ds climate -df t16-17 > ../climate/t16-17.json
python process.py -ds climate -df t17-18 > ../climate/t17-18.json

mkdir ../stock
python process.py -ds stock -df amzn > ../stock/amzn.json
python process.py -ds stock -df googl > ../stock/googl.json
python process.py -ds stock -df intc > ../stock/intc.json
python process.py -ds stock -df msft > ../stock/msft.json

mkdir ../astro
python process.py -ds radioAstronomy -df output_115_130 > ../astro/output_115_130.json
python process.py -ds radioAstronomy -df output_116_133 > ../astro/output_116_133.json
python process.py -ds radioAstronomy -df output_117_121 > ../astro/output_117_121.json
python process.py -ds radioAstronomy -df output_119_123 > ../astro/output_119_123.json

deactivate