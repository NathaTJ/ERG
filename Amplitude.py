#### This code will calculate the amplitude for all dependent variables of interest ###
#### awave and bwave amplitude; a- and b-wave implicit time, b/a ratio ##
#### It will genrate the following outputs:
############ Excel: 
#### 1.'MA_all_dep_var.xlsx'-- An excel sheet that has point-to-valley measurements, and amplitude measurements.
####    This sheet will be used by MA_descriptives.py and MA_ERG_spss
 
####### Code created by Nathalia Torres Jimenez -- updated on 2/21/2020


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


### Load dataset
directory = 'C:\\Users\\nator\\Documents\\Results\\Hurler\\p2v\\'
savefigsto= 'C:\\Users\\nator\\Documents\\Results\\Hurler\\Figures\\'
savedatato = 'C:\\Users\\nator\\Documents\\Results\\Hurler\\'
os.chdir(directory)## Changes directory to w dataset


#looop and stack up ALL TIMEPOINTS
########### Calculate Amplitudes ######
depvar = pd.DataFrame()
for tp in glob.glob("*.xlsx"):
	data = pd.read_excel(directory+tp) #load dataset
	data['a_amp'] = abs(data['a-peak']-data['Baseline'])/1000
	data['a_time'] = data['a-time']
	data['b_amp']= abs(data['b-peak']- data['a-peak'])/1000
	data['b_time']= data['b-time']
	data['ba_ratio']= data['b_amp']/data['a_amp']
	drop_labels = ['Baseline','a-time','a-peak','b-time','b-peak']
	x = data.drop(drop_labels, axis=1)
	depvar =depvar.append(x,ignore_index=True)

depvar.to_excel(savedatato+'Hurler_data.xlsx', index=False)

###############################################################
############### Descriptives Statistcs ########################
###############################################################

def scatterplots(str):
	####### Create descriptive categorical plates to visualize data
	##########
	#########

	### Select data from the testing adaptation condition desired
	### and seperate experimental groups of interest

	df= depvar.loc[depvar['Adaptation'] == str]
	mWT = df.query('Genotype == "WT" & Sex == "Male"')
	mKO = df.query('Genotype == "KO" & Sex == "Male"')
	mHT = df.query('Genotype =="HT" & Sex == "Male"')

	fWT = df.query('Genotype == "WT" & Sex == "Female"')
	fKO = df.query('Genotype== "KO" & Sex== "Female"')
	fHT	= df.query ('Genotype == "HT" & Sex=="Female"')

	group = {'mWT':mWT, 'mKO':mKO, 'mHT':mHT,'fWT': fWT,'fKO': fKO, 'fHT':fHT}
	dep_var = ['a_amp','a_time','b_amp','b_time','ba_ratio']
	sns.set_context("talk", font_scale=0.8)
	sns.set_style ("white")

	for key,group in group.items():
		for i in dep_var:
			fig= sns.catplot(x='Light_intensity',y=i,hue ='Animal', col= "Timepoint",data=group)
			plt.xticks(rotation=30, horizontalalignment='right')
			plt.savefig(savefigsto+str+'_'+key+"_distribution_"+"_"+i, dpi=150)
			plt.close('all')

			#fig2=sns.catplot(x='Light_intensity',y=i,kind='box',hue= 'Animal',col='Timepoint', data=group)
			#plt.xticks(rotation=30, horizontalalignment='right')
			#plt.savefig(savefigsto+str+'_'+key+"_boxplot_"+key+"_"+i, dpi1=150)
		plt.close('all')
plt.close("all")

scatterplots("MA")
scatterplots("DA")
	
	


############################################################### 
##################### Visualization ###########################
####################   amplitude    ###########################
###############################################################


#a_all=sns.catplot(x='Light_intensity', y='a_amp', hue='Genotype',ci="sd",
#			palette={"WT":"k","SRKO":"grey"},#
#            linestyles=["-", "--"], kind="point",data=a_amp, legend=False)
#plt.legend(['Both WT (n=13)','Both SR-/- (n=14)'],loc='upper right')
#plt.ylim(0,200)
#plt.title('a-wave amplitude - both sexes', loc='center',fontdict={'fontsize': 18})













##### Seperate Data into males and females

#female= a_amp.query('Sex=="Female"')
#male= a_amp.query('Sex=="Male"')

##### Seperate Data into males and females

#aFemale= a_amp.query('Sex=="Female"')
#aMale= a_amp.query('Sex=="Male"')

#atFemale= a_time.query('Sex=="Female"')
#atMale= a_time.query('Sex=="Male"')

#bFemale=b_amp.query('Sex=="Female"')
#bMale=b_amp.query('Sex=="Male"')

#btFemale=b_time.query('Sex=="Female"')
#btMale=b_time.query('Sex=="Male"')

#ba_ratioF=ba_ratio.query('Sex=="Female"')
#ba_ratioM =ba_ratio.query('Sex=="Male"')

##### Visualization ###
#sns.set_context("talk", font_scale=0.8)
#sns.set_style ("white")


##################### a-wave Visualization ####################
########################    amplitude    ######################
#a_all=sns.catplot(x='Light_intensity', y='a_amp', hue='Genotype',ci="sd",
#			palette={"WT":"k","SRKO":"grey"},#
#            linestyles=["-", "--"], kind="point",data=a_amp, legend=False)
#plt.legend(['Both WT (n=13)','Both SR-/- (n=14)'],loc='upper right')
#plt.ylim(0,200)
#plt.title('a-wave amplitude - both sexes', loc='center',fontdict={'fontsize': 18})

#a_male=sns.catplot(x='Light_intensity',y='a_amp', hue='Genotype', ci="sd",
#			kind= "point", data=aMale,
#			palette={"WT":"k", "SRKO":"b"},
#            linestyles=["-", "--"], legend=False)

#plt.legend(['Male WT (n=7)','Male SR-/- (n=7)'],loc="upper right")
#plt.ylim(0,200)
#plt.title('a-wave amplitude - males', loc='center',fontdict={'fontsize': 18})

#a_female=sns.catplot(x='Light_intensity',y='a_amp', hue='Genotype', ci="sd",
#			kind= "point", data=aFemale,
#			palette={"WT":"k", "SRKO":"r"},
 #           linestyles=["-", "--"],legend=False)

#plt.legend(['Female WT (n=6)','Female SR-/- (n=7)'], loc='upper right')
#plt.ylim(0,200)
#plt.title('a-wave amplitude - females', loc='center',fontdict={'fontsize': 18})


#a_all.savefig(fname+'_awave_amp_all.tif',dpi=120)
#a_male.savefig(fname+'_awave_amp_males.tif', dpi=120)
#a_female.savefig(fname+'_awave_amp_females.tif', dpi=120)

#plt.close('a_all')
#plt.close('a_male')
#plt.close('a_female')


########################    a-wave implicit time    ######################
#at_all=sns.catplot(x='Light_intensity', y='a_time', hue='Genotype', ci="sd",
#			palette={"WT":"k","SRKO":"grey"},
#            linestyles=["-", "--"], kind="point",data=a_time, legend=False)
#plt.legend(['Both WT (n=13)','Both SR-/- (n=14)'],loc='upper right')
#plt.ylim(10,40)
#plt.title('a-wave implicit time - both sexes', loc='center',fontdict={'fontsize': 18})

#at_male=sns.catplot(x='Light_intensity',y='a_time', hue='Genotype', ci="sd",
#			kind= "point", data=atMale,
#			palette={"WT":"k", "SRKO":"b"},
#            linestyles=["-", "--"], legend=False)

#plt.legend(['Male WT (n=7)','Male SR-/- (n=7)'],loc='upper right')
#plt.ylim(10,40)
#plt.title('a-wave implicit time - males', loc='center',fontdict={'fontsize': 18})


#at_female=sns.catplot(x='Light_intensity',y='a_time', hue='Genotype', ci="sd",
#			kind= "point", data=atFemale,
#			palette={"WT":"k", "SRKO":"r"},
#            linestyles=["-", "--"],legend=False)

#plt.legend(['Female WT (n=6)','Female SR-/- (n=7)'], loc='upper right')
#plt.ylim(10,40)
#plt.title('a-wave implicit time - females', loc='center',fontdict={'fontsize': 18})


#at_all.savefig(fname+'_awave_time_all.tif', dpi=120)
#at_male.savefig(fname+'_awave_time_males.tif', dpi=120)
#at_female.savefig(fname+'_awave_time_females.tif', dpi=120)

#plt.close('at_all')
#plt.close('at_male')
#plt.close('at_female')

