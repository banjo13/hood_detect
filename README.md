# hood_detect
hood_detect is a collection of Python3 scripts that takes the user from a HypoInverse2000 database file from the PNSN to creating the inputs for GrowClust (Trugman and Shearer, 2017). 
parse_hypo2000.py parses the PNSN HypoInverse2000 file so you can get earthquake location information, magnitudes, and uncertainties, and collects the phase arrival information. 

clean_arrivals.sh is a bash script to clean up the tmp.arr.csv file, and is run immediately aftr parse_hypo2000.py. outputs a csv of the arrivals. It uses vimclean.txt as the input for the sed commands to clean up the arr.csv. 

get_wigglesVertical.py downloads the waveforms for the Vertical (Z) components that were picked using obspy, and writes the arrival information in the header of each waveform
  Waveforms are saved as SAC files.

get_wigglesHorizantal.py does the same as get_wigglesVert, but for the horizontal components (E,N,1,2,T,R). 

TODO: add the eqcs scripts and the growclust scripts and descriptions. 


