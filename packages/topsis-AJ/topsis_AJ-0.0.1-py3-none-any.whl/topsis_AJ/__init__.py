import pandas as pd
import numpy as np
import sys

def file_path(file_name):
	try:
		file = pd.read_csv(file_name)
	except FileNotFoundError:
		print("Wrong file or file path")
		exit()

def check_argno():
	if len(sys.argv)!=5:
		print("Wrong number of arguments")
		exit()

def verifyweight(weights,columns):
	try:
		gotdata = weights[1]
	except IndexError:
		print("Weights should be separated by ','")
		exit()

	if len(weights)!=(columns-1):
		print("Wrong number of weights")
		exit()

def verifyimpact(impacts,columns):
	try:
		gotdata = impacts[1]
	except IndexError:
		print("Impact should be separated by ','")
		exit()

	for i in impacts:
		if i not in ["+", "-"]:
			print("impact can only be positive or negative")
			exit()
	if len(impacts)!=(columns-1):
		print("wrong number of impacts")
		exit()


def veifyinput(infile):
	file=infile.iloc[:,1:]
	if file.select_dtypes(include=['number','int','float']).shape[1]!=file.shape[1]:
		print("Convert these categorical columns into numerical: "+str(file.select_dtypes(include=['object']).columns))
		exit()

def takearguments():
	check_argno()
	file_path(sys.argv[1])
	infile=pd.read_csv(sys.argv[1])
	if infile.shape[1]>2:
		veifyinput(infile)
		verifyweight((sys.argv[2]).split(','),infile.shape[1])
		verifyimpact((sys.argv[3]).split(','),infile.shape[1])
		weights=(sys.argv[2]).split(',')
		weights=list(map(int,weights))
		impacts=(sys.argv[3]).split(',')
		output_file=sys.argv[4]
	else:
		print("wrong number of columns in input file")

	return infile,weights,impacts,output_file

def topsisrank(input,weights,impacts):
  labels=input.iloc[:,0]
  values=input.iloc[:,1:]
  values=np.array(values)
  for i in range(values.shape[1]):
    values[:,i]=values[:,i]/((values[:,i]**2).sum())

  values=values*weights

  max=[0]*(values.shape[1])
  min=[0]*(values.shape[1])
  for i in range(values.shape[1]):
    if impacts[i]=="+":
      max[i]=values[:,i].max()
      min[i]=values[:,i].min()
    elif impacts[i]=="-":
      max[i]=values[:,i].min()
      min[i]=values[:,i].max()

  max=np.array(max)
  min=np.array(min)

  s_plus=[0]*values.shape[0]
  s_minus=[0]*values.shape[0]
  for i in range(values.shape[0]):
    s_plus[i]=np.sqrt(((values[i]-max)**2).sum())
    s_minus[i]=np.sqrt(((values[i]-min)**2).sum())

  score=[0]*len(s_plus)
  for i in range(len(s_plus)):
    score[i]=s_minus[i]/(s_plus[i]+s_minus[i])

  output=input
  output['Topsis Score']=score
  output=output.sort_values(by='Topsis Score',ascending=False)

  output['Rank']=range(1,len(output)+1)

  output=output.sort_values(by=output.columns[0])

  return output
def topsis()
	if __name__ =='__main__':
		infile,weights,impacts,output_file=takearguments()
		output=topsisrank(infile,weights,impacts)
		output.to_csv(output_file,index=False)
