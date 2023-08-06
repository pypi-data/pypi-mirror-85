import pandas as pd
import numpy as np
import math as m
import sys
def top(arg):
	w = arg[1]
	im = arg[2]

	if len(arg) < 4:
		print("System arguments error")
		exit()

	try:
		w = w.split(",")
		im = im.split(",")
	except:
		print("Weight or Impact not comma seperated!")
		exit()
	w = [float(i) for i in w]
	for i in im:
		if not (i == "-" or i == "+"):
			print("Wrong Impact values")
			exit()
		
	#     file not found error
	try:
		df = pd.read_csv(arg[0])
	except:
		print("file not found")
		exit()

	df = df.set_index("Model")
		
	#     checking for string values
	for i in range(len(df)):
		for j in range(len(df.columns)):
			if isinstance(df.iloc[i, j], str):
				print("Data contains string value")
				exit()
				
	#     checking length of columns
	if len(df.columns) < 3:
		print("Less than 3 columns inputted")
		exit()
		
	if len(w) != len(im) or len(im) != len(df.columns):
		print("Lengths of columns, weights and impact do not match")
		exit() 
		

	a=df.copy()

	row=a.shape[0]
	col=a.shape[1]

	print(a)
	#normalizing matrix
	for j in range(0,col):
		denominator=0
		for i in range(0,row):
			denominator=denominator+(a.iat[i,j]*a.iat[i,j])
		s=m.sqrt(denominator)
		for i in range(0,row):
			a.iat[i,j]=a.iat[i,j]/denominator
			
	#multiplying by weights
	for j in range(0,col):
		for i in range(0,row):
			a.iat[i,j]=a.iat[i,j]*w[j]
			
	#calculating vj+ and vj-
	vj_p=[]
	vj_n=[]
	for j in range(0,col):
		if(im[j]=='+'):
			vj_p.append(max(a.iloc[:,j]))
			vj_n.append(min(a.iloc[:,j]))
		elif(im[j]=='-'):
			vj_p.append(min(a.iloc[:,j]))
			vj_n.append(max(a.iloc[:,j]))

	#calculating si+ and si-
	si_p=[]
	si_n=[]
	for i in range(0,row):
		x=0
		y=0
		for j in range(0,col):
			x=x+(a.iat[i,j]-vj_p[j])*(a.iat[i,j]-vj_p[j])
			y=y+(a.iat[i,j]-vj_n[j])*(a.iat[i,j]-vj_n[j])
		si_p.append(m.sqrt(x))
		si_n.append(m.sqrt(y))  
		
	#calculating topsis score
	p_score=[]
	for i in range(0,row):
		p_score.append(si_n[i]/(si_n[i]+si_p[i]))
		

		
	#calculating rank
	rank=[]
	p=p_score.copy()
	for i in range(0,row):
		rank.append(0);
	r=1;
	for i in range(0,row):
		d=p_score.index(max(p)) 
		p[d]=-1
		rank[d]=r
		r=r+1
		
	final=pd.DataFrame(df)
	final['Topsis Score']=p_score
	final['Rank']=rank
	print(final)
	final.to_csv(arg[3])