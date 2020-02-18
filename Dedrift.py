#### This script replaces original files with dedrifted data 
#### a mouse electrophysiological dataset
#### (especifically electroretinograms recorded with Espion system)
#### I organize my files by experimental group, which is a between subject factor. Each unique and can not be anything else
#### For instance, male wild-type (mWT) and male knock-out (mKO) mice will be names of subfolders within project, that I refer to as group
####  Within each group folder (e.g., mWT), each file is labeled from 1 to n (total sample size withing that group) 
#### And corresponds to a single subject within that group. 
#### To summarize, in a preject, I have experimantal groups, and the data from each subject, resides in one of these experimental groups.


## upload necessary libraries
import numpy as np
import pandas as pd
import glob
import os
from pathlib import Path
from scipy import signal

home = 'C:\\Users\\nator\\Documents\Python Scripts\\' ## The residence of your python scripts


directory = 'C:\\Users\\nator\\Desktop\\hurlerDA_ERG_copy\\TP1'## The residence of the COPY of your ERG dataset 
os.chdir(directory)## Changes directory to w dataset

groups= list(Path.cwd().glob('*')) ## mWT, mKO,mHT,fWT,fKO,fHT

for group in groups:
### Change directory necessary to save files in the proper group
	os.chdir(group)
	files = list(group.glob('*')) ## all subjects (files) within that group
	for file in files:
		df = pd.read_excel(file) 
		labels = df.iloc[:2:,:] 
		info= df.iloc[2:,:14] ## Electrophys recording info
		info.reset_index(inplace=True,drop=True) 
		
		### Slicing the segment with ERG singal **this includes time**
		RawERG = df.iloc[2:,14:] *(1/1000) ## convert to uV, and slice only the part with the signal
		detrend= signal.detrend(RawERG,axis=0) ##  
		detrend = pd.DataFrame(detrend) 
		
		### joining original recording information to detrended dataset
		df2 = info.join(detrend)
		df2.set_axis(df.columns,axis=1, inplace=True)
		### Add the original header/labels
		result=pd.concat([labels,df2])
		### Replace original with detrended info
		result.to_excel(file.name, index=False)
## This part not necessary, but let's you know when python finished the last file for a grou
	print('finished '+file.name)	
print('all done')
