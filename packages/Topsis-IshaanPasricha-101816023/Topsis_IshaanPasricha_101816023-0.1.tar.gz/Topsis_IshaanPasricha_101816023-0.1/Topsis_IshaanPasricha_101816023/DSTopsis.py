# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 14:39:46 2020

@author: admin
"""
import sys
import pandas as pd
import numpy as np
import os


def checkParameter():
	parameters = sys.argv
	if(len(parameters)!=5 ):
		print("Please provide all the parameters...\n")
		return 0
	else:
		for filename in sys.argv[1:]:
			if(filename.endswith('.csv')):
				File_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
				if os.path.exists(File_path) != 1:
					print('File with filename %s doesnot exist in root directory!\n' %(filename))
					print('PS: Current Directory: ',os.path.abspath(__file__))
					print('\nTerminating...')
					return 0
				else:
					fileData = pd.read_csv(filename)
					if len(fileData.columns) <3:
						print('File with filename %s contains less than 3 columns\nTerminating...' %(filename))
						return 0
					else:
						impacts = sys.argv[3].split(",")
						weights = sys.argv[2].split(",")
						for i in range(0,(fileData.shape[0])):
							for j in range(1,len(weights)+1):
								try:
									fileData.iloc[i,j] = int(fileData.iloc[i,j])
								except:
									print("File Contains non-numeric values.\n Terminating...")
									return 0
						if (len(sys.argv[2].split(",")) == len(sys.argv[3].split(",")) and len(sys.argv[3].split(",")) == fileData.shape[1]-1):
							
							for i in impacts:
								if i == "+" or i == "-":
									continue
								else:
									print("Impact must be '+' or '-'\n Terminating...")
									return 0
							for i in weights:
								try:
									i = int(i)
								except:
									print("Weights must be integer and separated by a ','.\nTerminating...")
									return 0
							
						else:
							print("Incorrect input. Length of impact,weights and number of columns(except 1) must be equal. \n Terminating...")
			else:
				print('File with filename : %s is not supported(must end with *.csv )\nTerminating...' %(filename))
				return 0
			return 1

print('\n')

if checkParameter() == 0:
	exit()


filename = sys.argv[1]
weights = sys.argv[2].split(",")
impacts = sys.argv[3].split(",")
outputFile = sys.argv[4]
totalWeight =0



for i in range(len(weights)):
	totalWeight= totalWeight+int(weights[i])
#resultFilename = sys.argv[4]
fileData = pd.read_csv(filename)
CopyFile =pd.read_csv(filename)
minMax = list()
for j in range(1,len(weights)+1):
	impact = impacts[j-1];
	SquareSum=0
	sumOfValue =0
	best=0
	worst=0
	if(impact == "+"):
		best = 0
		worst =10000000
	else:
		best = 100000000
		worst = 0
	for i in range(0,(fileData.shape[0])):
		SquareSum= SquareSum + fileData.iloc[i,j]*fileData.iloc[i,j]
	SquareSum = np.sqrt(SquareSum)
	for i in range(0,(fileData.shape[0])):
		if impact == "+": 
			fileData.iloc[i,j] = fileData.iloc[i,j]*(int(weights[j-1]))/(SquareSum*totalWeight)
			if(fileData.iloc[i,j]>best):
				best = fileData.iloc[i,j]
			if(fileData.iloc[i,j]<worst):
				worst = fileData.iloc[i,j]
		else:
			fileData.iloc[i,j] = fileData.iloc[i,j]*(int(weights[j-1]))/(SquareSum*totalWeight)
			if(fileData.iloc[i,j]>worst):
				worst = fileData.iloc[i,j]
			if(fileData.iloc[i,j]<best):
				best = fileData.iloc[i,j]
	
	minMax.append([best,worst])
# Sj+ and Sj-
#print(minMax)
performance = list()
for i in range(0,(fileData.shape[0])):
	SPlus = 0
	SMinus = 0
	for j in range(1,len(weights)+1):
#		print("File ",fileData.iloc[i,j] )
#		print("minMax ",minMax[j-1][0])
		t = fileData.iloc[i,j] - minMax[j-1][0]
#		print("t",t)
		SPlus = SPlus+pow(t,2)
		t=(fileData.iloc[i,j]-minMax[j-1][1])
		SMinus = SMinus+pow(t,2)
	SPlus = np.sqrt(SPlus)
	SMinus = np.sqrt(SMinus)
	performance.append(SMinus/(SPlus+SMinus))
CopyFile["Score"] = performance
CopyFile["Rank"] = CopyFile["Score"].rank(ascending = False)

CopyFile.to_csv(outputFile)
print("File saved successfully...\n")

	
			
		
		
	
		
	
			
		
		
	
