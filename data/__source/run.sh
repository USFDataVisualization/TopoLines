#!/bin/bash

. venv/bin/activate

mkdir ../eeg
python process.py -ds eeg -df chan01 > ../eeg/eeg_chan01.json
python process.py -ds eeg -df chan07 > ../eeg/eeg_chan07.json
python process.py -ds eeg -df chan14 > ../eeg/eeg_chan14.json
python process.py -ds eeg -df chan21 > ../eeg/eeg_chan21.json

mkdir ../climate
python process.py -ds temperature -df t14-15 > ../climate/climate_14-15.json
python process.py -ds temperature -df t15-16 > ../climate/climate_15-16.json
python process.py -ds temperature -df t16-17 > ../climate/climate_16-17.json
python process.py -ds temperature -df t17-18 > ../climate/climate_17-18.json

mkdir ../stock
#python process.py -ds stock -df amzn > ../stock/stock_amzn.json
#python process.py -ds stock -df googl > ../stock/stock_goog.json
#python process.py -ds stock -df intc > ../stock/stock_intc.json
#python process.py -ds stock -df msft > ../stock/stock_msft.json
python process.py -ds stock2 -df amzn > ../stock/stock_amzn.json
python process.py -ds stock2 -df goog > ../stock/stock_goog.json
python process.py -ds stock2 -df intc > ../stock/stock_intc.json
python process.py -ds stock2 -df tsla > ../stock/stock_tsla.json

mkdir ../astro
python process.py -ds radioAstronomy -df output_115_120 > ../astro/astro_115_120.json
python process.py -ds radioAstronomy -df output_115_123 > ../astro/astro_115_123.json
python process.py -ds radioAstronomy -df output_115_128 > ../astro/astro_115_128.json
python process.py -ds radioAstronomy -df output_116_134 > ../astro/astro_116_134.json

deactivate
