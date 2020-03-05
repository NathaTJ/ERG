#################################################################################################################
#### This code calucates the dependent variables of the electroretigram recorded at different light-adaptation conditions
#### It visualzes the response of every animal in a given group across time
#### and calculates statistics - 2waymixANOVA for experiment hightlighted below
####
#### Experiment: Six groups of animals had 3 different types of ERG recorded, 3 different times.
#### Investigator interested in knowing if there is a difference between the different groups with time for each type of ERG ('adaptation') at every flash-strength ('light intensity')
####
#### Independent Variables
#### Groups [between-subject factor] : male wildtype (mWT), female Wildtype (fWT), male knockout(mKO), female knockout (fKO) male heterozygous (mHT), female heterozygous (fHT)
#### Timepoint [within-subject factor]: the different time points at which the ERG was recorded for the same animal (TP1, TP2, TP3)
#### Adaptation of ERG [within-subject factor]: 3 different types of ERG recorded at 3 different levels of retinal adaptation [Light-adapted("LA"), Mesopic-adapted ("MA"), Dark-adapted("DA")]
#### Light-intensity[within-subject factor]: flash-strength series (increasing increments of flash brightness onto the eye) // Each type of ERG has their unique flash-strength series
####
#### Dependent Variables:
#### The low-frequency dependent variables are: 
#### 	1) a-wave amplitude
####	2) b-wave amplitude
####	3) a-wave implicit time
####	4) b-wave implicit time
#### 
#### 
#### Dataset: processed-ERGs, where the ERG has been filtered and x,y coordinates for a- and b-waves have been extracted
####		  That file is refereed to as point-to-valley measurements (p2v)
#### 
#### 
#### Code created by Nathalia Torres Jimenez -- updated on 3/05/2020



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import pingouin as pg


##### Inputs location
directory = 'C:\\Users\\nator\\Documents\\Results\\Hurler\\p2v\\' ## Location where your peak-to-valley data is stored

##### Outputs location
savedatato = 'C:\\Users\\nator\\Documents\\Results\\Hurler\\' ## Location to store the dependent variables calculated form peak-to-valley measurements
savefigsto= 'C:\\Users\\nator\\Documents\\Results\\Hurler\\Figures\\' ## Location to store the figs from descriptive_scatter
savestatsto = 'C:\\Users\\nator\\Documents\\Results\\Hurler\\2mixANOVA\\' ## Location to store results from twoMixANOVA

os.chdir(directory)## Changes directory to where you stored your datasets. Use if your Python Scripts are in different folder from your dataset




##### Calculate dependent variables and merge different adaptation conditions into a sigle dataframe #####


depvar = pd.DataFrame()  # set a dataframe where you will place dependent variables for all adapatation conditions which you tested

for tp in glob.glob("*.xlsx"): # gets all peak-to-valley excel files from all light levels of adaptation
	data = pd.read_excel(directory+tp) #load dataset
	data.fillna(0)
	data['a_amp'] = abs(data['a-peak']-data['Baseline'])/1000 # a-wave amplitude calculation with nV to uV conversion 
	data['a_time'] = data['a-time'] # a-wave implicit time
	data['b_amp']= abs(data['b-peak']- data['a-peak'])/1000 #b-wave amplitude caluclation with nV to uV conversion
	data['b_time']= data['b-time']# b-wave implicit time
	drop_labels = ['Baseline','a-time','a-peak','b-time','b-peak'] #Peak-valley (x,y) coordinates; not necessasry in df moving fward
	x = data.drop(drop_labels, axis=1)
	depvar =depvar.append(x,ignore_index=True) #join all


####### Create a column for the independent variable (factor): Groups ##########

group_labels=[]
for i in depvar.Animal:
	group_labels.append(i[:3]) ## grab the first 3 positoins
	
depvar['Group'] = group_labels ## insert new group labels in df


depvar.to_excel(savedatato+'Hurler_data.xlsx', index=False)# Df with all dependent variables across all light-adaptation conditions

def descriptive_scatter(adaptation):
	""" Saves scatterplots for each tested group across time for all dependent variables in a folder called 'Figures'
		Each point reflects a given animal within that group. Same color is used for the same animal across time.
		Picture files (.png) are created following this naming convention
			Ligh-adapatationp_groupmembership_DescriptiveScatter_dependentvariable 
			example "MA_mWT_DescriptiveScatter_a_amp.png"
	
	User specifies:
	First parameter (str): Adaptation condition in which the ERG was recorded (Dark-adapted ('DA'), Light-adapted ('LA'), and Mesopic-adapted ('MA'))
	
	Returns: Many png files
	
	"""

	df= depvar.loc[depvar['Adaptation'] == adaptation]
	mWT = df.loc[df['Group'] == "mWT"]
	mKO = df.loc[df['Group'] == "mKO"]
	mHT = df.loc[df['Group'] == "mHT"]

	fWT = df.loc[df['Group'] == "fWT"]
	fKO = df.loc[df['Group'] == "fKO"]
	fHT	= df.loc[df['Group'] == "fHT"]

	group = {'mWT':mWT, 'mKO':mKO, 'mHT':mHT,'fWT': fWT,'fKO': fKO, 'fHT':fHT}
	dep_var = ['a_amp','a_time','b_amp','b_time','ba_ratio']
	sns.set_context("talk", font_scale=0.8)
	sns.set_style ("white")

	for key,group in group.items():
		for i in dep_var:
			fig= sns.catplot(x='Light_intensity',y=i,hue ='Animal', col= "Timepoint",data=group)
			plt.xticks(rotation=30, horizontalalignment='right')
			plt.savefig(savefigsto+str+'_'+key+"_DescriptiveScatter_"+"_"+i, dpi=150)
			plt.close('all')

		plt.close('all')
plt.close("all")

#scatter("MA")
#scatter("DA")
#scatter("LA")


def twoMixANOVA(adaptation, var):
	""" Calculates and prints 2-way Mix ANOVA results for every light intensity in a specified light-adaptation series
		Group is the between-subject factor: male wildtype (mWT), female Wildtype (fWT), male knockout(mKO), female knockout (fKO) male heterozygous (mHT), female heterozygous (fHT)
		Time is the within-subject factor: the different time points at which the ERG was recorded for the same animal (TP1, TP2, TP3)
	
	User specifies:
	First parameter (str): Adaptation condition in which the ERG was recorded (Dark-adapted ('DA'), Light-adapted ('LA'), and Mesopic-adapted ('MA'))
	Second Parameter (var): Dependent variable to calculate ('a_amp', 'b_amp','a_time', 'b_time')
	
	Returns 2-way mix ANOVA table

	"""
	df_adaptation = depvar.loc[depvar['Adaptation'] == adaptation]
	grouped = df_adaptation.groupby('Light_intensity')
	results = pd.DataFrame()
	#light= []
	
	for name, group in df_adaptation.groupby('Light_intensity'): 
		light_df= pd.DataFrame(data=group, columns=group.columns) #Place the tuples created with groupby into a new Dataframe
		#Results.append(name)
		aov = pg.mixed_anova(data=light_df, dv=var, between='Group', within='Timepoint', subject='Animal', correction=False) # correction true/false depends on whether you have a balanced design or not
		results=results.append(aov)
		pg.print_table(aov)
	
	results.to_excel(savestatsto+adaptation+'_'+'_'+var+'.xlsx')
	return results
	
#twoMixANOVA('MA','a_amp')
#twoMixANOVA('MA','b_amp')
#twoMixANOVA('MA','a_time')
#twoMixANOVA('MA','b_time')

#twoMixANOVA('LA','a_amp')
#twoMixANOVA('LA','b_amp')
#twoMixANOVA('LA','a_time')
#twoMixANOVA('LA','b_time')

#twoMixANOVA('DA','a_amp')
#twoMixANOVA('DA','b_amp')
#twoMixANOVA('DA','a_time')
#twoMixANOVA('DA','b_time')

