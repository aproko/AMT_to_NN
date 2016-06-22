#!bin/bash

#Make sure your AMT data is sorted by HIT ID
python extract_data.py $1

#Ensure we don't have any duplicates
python normalize.py

#Puts the data into the form Label \t Text which we can then use to train our neural net
python to_nn_input.py