##------------------------------------------------------------------------------------##

## Please kindly cite the relevant paper of the author if the data are helpful to you.
## Author contact:
## Name: Wang Zhu
## Email: wang4027146@foxmail.com; zhuwang@tongji.edu.cn
## Orcid: 0000-0003-3844-8014
## Researchgate: https://www.researchgate.net/profile/Wang-Zhu-13

session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)
from math import*
from abaqus import*
from abaqusConstants import*
from caeModules import*
from driverUtils import executeOnCaeStartup
import numpy as np
executeOnCaeStartup()


##-----------------------------------------Preparation-----------------------------------##

## Please prepare a series of coordinate file of the nodes, each represents all nodes in one part instance

## Name them like: "anchor1", "anchor2", "anchor3",......

## For instance, the file folder provides a case file named "anchor1.txt", including 88 nodes from an anchor, also from the concrete.

## If one has N txt files, one needs to run this script for N times.

##-----------------------------------------Basic information-----------------------------------##
MYMODEL=str(str(getInput('Please enter the name of the model')))    #####input the model name in the ABAQUS GUI
name_part=['anchor-1']                                              ############All names of the anchors in Assembly model
num_part=str(str(getInput('name of txt file')))                     ##### The serial number of a txt file.
Part_sub=name_part[int(num_part)-1] 
# Part_sub='anchor-1' 
Part_host=str('concrete-1')                                         ##### The name of the concrete instance
name_txt='anchor'+str(int(num_part))                                #the name of the txt file
LENGTH=0.05


##-------------------------------------get the 3D cooredinats from txt file to list0---------------------------------##
my_data = np.loadtxt('F:\\xt\\Desktop\\TTF\\'+name_txt+'.txt')        #the path & the name of the txt file
anchor= my_data.tolist()
num_0=len(anchor)
list0=[]
for t in range(num_0):
  list0.append((t,anchor[t][0],anchor[t][1],anchor[t][2]))

##--------------------------------get the 3D cooredinats of all nodes in the Part_sub to list1-----------------------##
a = mdb.models[MYMODEL].rootAssembly
n1 = a.instances[Part_sub].nodes
list1 = []
num_1 = len(n1)
for i in range(num_1):
  list1.append((i,n1[i].coordinates[0],n1[i].coordinates[1],n1[i].coordinates[2]))

##--------------------------------get the 3D cooredinats of all nodes in the Part_host to list2-----------------------##
a = mdb.models[MYMODEL].rootAssembly
n2 = a.instances[Part_host].nodes
list2 = []
num_2 = len(n2)
for j in range(num_2):
  list2.append((j,n2[j].coordinates[0],n2[j].coordinates[1],n2[j].coordinates[2]))


##--------------------------find the node names on the Part_sub and Part_host, given list0-----------------------##
list3 = []
for tt in range(num_0):
  for ii in range(num_1):
    if pow(((list1[ii][1]-list0[tt][1])**2+(list1[ii][2]-list0[tt][2])**2+(list1[ii][3]-list0[tt][3])**2),0.5) < float(LENGTH):
      MM=ii
    else:
      continue
  for jj in range(num_2):
    if pow(((list2[jj][1]-list0[tt][1])**2+(list2[jj][2]-list0[tt][2])**2+(list2[jj][3]-list0[tt][3])**2),0.5) < float(LENGTH):
      NN=jj
    else:
      continue
  list3.append((list1[MM][0]+1,list2[NN][0]+1))


##-------------establish node conbinations for the nodes with the same coordi. but different isntance--------------##
list4 = []
num_3 = len(list3)
for iii in range(num_3):
  n1=a.instances[Part_sub].nodes
  n2=a.instances[Part_host].nodes
  list4.append((n1[list3[iii][0]-1],n2[list3[iii][1]-1]))


##-------------------------------------------------Create wires-----------------------------------------------------##
a = mdb.models[MYMODEL].rootAssembly
a.WirePolyLine(points=(list4), mergeType=IMPRINT, meshable=OFF)
a = mdb.models[MYMODEL].rootAssembly
e1 = a.edges
edges1 = e1[0:num_3]
a.Set(edges=edges1, name='Wire-'+str(int(num_part)))
print('Total number of created wires :',num_3)
print('Wires creat successfully')