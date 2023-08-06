# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:55:54 2020

@author: goels
"""


#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import sys
def just_import_this_fxn_for_whole_topsis_result():
#Correct number of Parameters
	if(len(sys.argv)!=5):
	    raise Exception('Kindly Enter correct number of parameters')


#File Not found Exception Handled
	try:
	    df=pd.read_csv(sys.argv[1])
	except FileNotFoundError:
	    print('Exception -- File Not found error')
	    exit()
 



	rows=df.shape[0]
	column=df.shape[1]


#Input file must contain three or more columns
	if column <3:
	    raise Exception ('No of columns in input file must be >=3')




#Handling of non numeric Characters from Column 2 to Last Column
	for i in range (0,rows):
	    for j in range (1,column):
        	try :
	            df.iloc[i,j]=float(df.iloc[i,j])
        	except:
	            raise Exception('From Column 2 to last Column only Enter numeric values only')



#Weight must be seperated by comma   
	weights=[]
	for i in range(0,len(sys.argv[2])):
	    if(i%2==1):
	        if( sys.argv[2][i]!=','):
        	    raise Exception('Input of weights must be seperated by comma')
	    else :
        	try:
	            weights=weights+[float(sys.argv[2][i])]
        	except:
	            raise Exception('Weights can be of type float or int not of the type you entered')




#Impacts must be either +ive or -ive and seperated by comma
	criteria=[]

	for i in range(0,len(sys.argv[3])):
	    if(i%2==1):
        	if( sys.argv[3][i]!=','):
	            raise Exception('Input of Criteria must be seperated by comma')
	    else :
        	if(sys.argv[3][i]=='+' or sys.argv[3][i]=='-'):
	            criteria=criteria+[sys.argv[3][i]]
	        else:
        	    raise Exception('Impacts can only be +ive or -ive')
            

#Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.
	if ((len(weights) != len(criteria)) or (len(weights) != column-1) or (len(criteria)!=column-1)):
	    raise Exception('Number of weights, number of impacts and number of columns from 2nd to last must be same')


#Calculation of root of sum of squares
	root_of_sum_of_squares=[]
	for i in range(1,column):
	    x=df.iloc[:,i]
	    y=sum(x*x)                                                       #Calculating Sum of squares
	    root_of_sum_of_squares=root_of_sum_of_squares+[(y**0.5)]        #Calculating Root of Sum of squares
	#print(root_of_sum_of_squares)




#Creation of Normalised_matrix
	normalised_matrix=pd.DataFrame(df.iloc[:,0])
	i=0
	for col in df.columns:
	    if i!=0:
	        normalised_matrix[col]=df.iloc[:,i]/root_of_sum_of_squares[i-1]
	    i=i+1





#Creation of Weighted_normalised_decision_matrix
	weighted_normalised_decision_matrix=pd.DataFrame(normalised_matrix.iloc[:,0])
	i=0
	for col in normalised_matrix.columns:
	    if i!=0:
	        weighted_normalised_decision_matrix[col]=normalised_matrix.iloc[:,i]*weights[i-1]
        #print(w[i-1])
	    i=i+1






#Making the list of ideal best and ideal worst
	ideal_best=[]
	ideal_worst=[]
	for i in range(0,column-1):
	    if(criteria[i]=='+'):
	        ideal_best=ideal_best+[max(weighted_normalised_decision_matrix.iloc[:,i+1])]
	        ideal_worst=ideal_worst+[min(weighted_normalised_decision_matrix.iloc[:,i+1])]
	    elif criteria[i]=='-':
	        ideal_best=ideal_best+[min(weighted_normalised_decision_matrix.iloc[:,i+1])]
	        ideal_worst=ideal_worst+[max(weighted_normalised_decision_matrix.iloc[:,i+1])]
#print(ideal_best)
#ideal_worst




#Euclidian Distance Calculation for ideal best and worst
	euclidian_distance_ideal_best=[]
	euclidian_distance_ideal_worst=[]
	for i in range(0,rows):
	    eu=0
	    eu1=0
	    for j in range(0,column-1):
	        eu=eu+(weighted_normalised_decision_matrix.iloc[i,j+1]-ideal_best[j])*(weighted_normalised_decision_matrix.iloc[i,j+1]-ideal_best[j])
	        eu1=eu1+(weighted_normalised_decision_matrix.iloc[i,j+1]-ideal_worst[j])*(weighted_normalised_decision_matrix.iloc[i,j+1]-ideal_worst[j])
	    euclidian_distance_ideal_best=euclidian_distance_ideal_best+[eu**0.5]
	    euclidian_distance_ideal_worst=euclidian_distance_ideal_worst+[eu1**0.5]
#print(euclidian_distance_ideal_best)
#print(euclidian_distance_ideal_worst)




#Sum of Euclidian distance of ideal best and ideal worst
	euclidian_distance_both=[]
	for i in range(0,rows):
	    euclidian_distance_both=euclidian_distance_both+[euclidian_distance_ideal_best[i]+euclidian_distance_ideal_worst[i]]
#euclidian_distance_both




#Calculating the performance score
	performance_score=[]
	for i in range(0,rows):
	    performance_score=performance_score+[euclidian_distance_ideal_worst[i]/euclidian_distance_both[i]]
#print(performance_score)




#Calculating the rank based on Performance score
	rank=[]
	for i in range(0,rows):
	    count=0
	    for j in range (0,rows):
	        if ( i != j and performance_score[i]<performance_score[j]):
	            count=count+1
	    rank=rank+[count+1]
#rank





#Storing the Performace Score and Rank in df
	df['TOPSIS SCORE']=performance_score
	df['RANK']=rank
	print("The final result that is Performance score and rank of the data is -->\n")
	print(df)


#Storing the result in output file whose name is provided by user
	df.to_csv(sys.argv[4],index=False)
	print("All the Steps of Topsis are done!!!")
	print("See the output file in the desired folder!!!")






