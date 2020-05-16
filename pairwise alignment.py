# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZWx76UMUWyERIpbhohqhm75uBMv-e0MI

CSC 464 2.0 Computational Biology


Assignment 1

Index Number:AS2016467

# Part 1: Needleman-Wunsch Algorithm for Global Alignment

def scoring :function for scoring
"""

import numpy as np
from string import*

Match=+1  # default values for Match,Mismatch,Gap
Mismatch=-1
Gap=-1

def scoring(match,misatch,gap):#function for initialize penalties for match,mismatch and gap 
  Match=match 
  Mismatch=mismatch
  Gap=gap

"""function to find alignment paths"""

seq1="ATTAC"
seq2="AATTC"


m= len(seq1)+1 #Initiation Matrix Size (Rows)
n = len(seq2)+1 #Initiation Matrix Size (Columns)
M= [[[[None] for i in range(2)] for i in range(n)] for i in range(m)] # Initiating Score Matrix
Gap_char = '-'#Character to Represent Gaps in Final Alignemnts
Align_paths= [] #Initiating List of Discovered aln Pathways



def find_each_route(c_i,c_j,path=''): #Nested function to discover new aln pathways
    global Align_paths 
    i = c_i 
    j = c_j 
    if i == 0 and j==0:       #If come back to the first cell
        Align_paths.append(path) 
        return 2 
    dir_t = len(M[i][j][1]) #number of maximum values in o_val
    while dir_t<=1: 
        n_dir = M[i][j][1][0] if (i != 0 and j != 0) else (1 if i == 0 else (3 if j==0 else 0)) 
        path = path + str(n_dir) 
        if n_dir == 1:  #Left 
            j=j-1
        elif n_dir == 2: #diagonal
            i=i-1
            j=j-1
        elif n_dir == 3: #up
            i=i-1
        dir_t = len(M[i][j][1])
        if i==0 and j==0:
            Align_paths.append(path) #when come to the initial point; then append
            return 3
    if dir_t>1:
        for dir_c in range(dir_t):
            n_dir = M[i][j][1][dir_c] if (i != 0 and j != 0) else (1 if i == 0 else (3 if j==0 else 0))
            tmp_path = path + str(n_dir)
            if n_dir == 1:
                n_i = i
                n_j=j-1
            elif n_dir == 2:
                n_i=i-1
                n_j=j-1
            elif n_dir == 3:
                n_i=i-1
                n_j = j
            find_each_route(n_i,n_j,tmp_path)
    return len(Align_paths)

"""def needle:function for needle-wunsch algorithm"""

#Main Code

#matrix Evalution[start]

def needle(seq1,seq2):
  for i in range(m):  
    M[i][0] = [Gap*i,[]] #find values to initialize first column

  for j in range(n):
     M[0][j] = [Gap*j,[]] #find values to initialize first row

  for i in range(1,m):
    for j in range(1,n):
        score = Match if (seq1[i-1] == seq2[j-1]) else Mismatch #check whether match or mismatch
        left = M[i][j-1][0] + Gap                               #value of left cell of current cell
        diagonal = M[i-1][j-1][0] + score                       #value of diagonal cell of current cell
        up = M[i-1][j][0] + Gap                                 #value of up cell of current cell
        o_val = [left,diagonal,up]                              #o_val is an array of left,diagonal and up
        M[i][j] = [max(o_val), [i+1 for i,v in enumerate(o_val) if v==max(o_val)]] # up = 1, diagonal = 2, left = 3
        
  #Matrix Evaulation [end]


  Best_Score = M[i][j][0]
  print(Best_Score) 
  score = Best_Score
  l_i = i      #store index in temperal variables
  l_j = j
  Alignments= [] #create an array for Alignments
  tot_aln = find_each_route(i,j) #return number of align paths
  aln_count = 0

  #Compiling alignments based on discovered matrix pathways
  for elem in Align_paths:
    i = l_i-1   
    j = l_j-1
    side_aln = '' 
    top_aln = ''
    step = 0
    aln_info = []
    for k in range(len(elem)):
        n_dir = elem[k]
        score = M[i+1][j+1][0]
        step = step + 1
        aln_info.append([step,score,n_dir])
        if n_dir == '2': # If diagonl
            side_aln = side_aln + seq1[i]
            top_aln = top_aln + seq2[j]
            i=i-1
            j=j-1
        elif n_dir == '1': # If up
            side_aln = side_aln + Gap_char
            top_aln = top_aln + seq2[j]
            j=j-1
        elif n_dir == '3':  #If left
            side_aln = side_aln + seq1[i]
            top_aln = top_aln + Gap_char
            i=i-1
    aln_count = aln_count + 1
    Alignments.append([top_aln,side_aln,elem,aln_info,aln_count])

  print('Total Alignments: ' + str(len(Alignments)))
  print('Overall Score: '+str(Alignments[0][3][0][1])+'\n')
  for elem in Alignments:
    print(elem[0][::-1]+'\n'+elem[1][::-1]+'\n') #print Alignments

"""Testcase"""

needle("ATTAC","AATTC")

"""# Part 2-Smith-Waterman Algorithm for Local Alignment

function for find alignment paths
"""

Seq1="ACATAG"
Seq2="AATG"


m= len(Seq1)+1 #Initiation Matrix Size (Rows)
n = len(Seq2)+1 #Initiation Matrix Size (Columns)
M= [[[[None] for i in range(2)] for i in range(n)] for i in range(m)] # Initiating Score Matrix
Gap_char = '-'#Character to Represent Gaps in Final Alignemnts
Align_paths= [] #Initiating List of Discovered aln Pathways



def find_each_route(c_i,c_j,path=''): #Nested function to discover new aln pathways
    global Align_paths 
    i = c_i 
    j = c_j 
    if M[i][j][0]==0:      #If come back to the first cell
        Align_paths.append(path) 
        return 2 
    
    while M[i][j][1]!=4: 
        n_dir = M[i][j][1][0] if (i != 0 and j != 0) else (1 if i == 0 else (3 if j==0 else 4)) 
        path = path + str(n_dir) 
        if n_dir == 1:  #Left 
            j=j-1
        elif n_dir == 2: #diagonal
            i=i-1
            j=j-1
        elif n_dir == 3: #up
            i=i-1
        dir_t = len(M[i][j][1])
        if M[i][j][0]==0:
            Align_paths.append(path) #when come to the initial point; then append
            return 3
    

    
    return len(Align_paths)

"""def waterman:function for smithwaterman algorithm"""

#Main Code

#matrix Evalution[start]

def waterman(Seq1,Seq2):
  for i in range(m):  
    M[i][0] = [0,[4]] #find values to initialize first column

  for j in range(n):
     M[0][j] = [0,[4]] #find values to initialize first row

  Best_Score=0
  for i in range(1,m):
    for j in range(1,n):
        score = Match if (Seq1[i-1] == Seq2[j-1]) else Mismatch #check whether match or mismatch
        left = M[i][j-1][0]+ Gap                               #value of left cell of current cell
        diagonal = M[i-1][j-1][0] + score                       #value of diagonal cell of current cell
        up = M[i-1][j][0]+ Gap                                 #value of up cell of current cell
        o_val = [left,diagonal,up,0]                              #o_val is an array of left,diagonal and up
        M[i][j] = [max(o_val), [i+1 for i,v in enumerate(o_val) if v==max(o_val)]] # up = 1, diagonal = 2, left = 3,0=4
        
        if Best_Score<=M[i][j][0]:
            Best_Sc0re=M[i][j][0]
  #Matrix Evaulation [end]



  print(Best_Score) 
  score = Best_Score

  for i in range(1,m):
    for j in range(1,n):
      if(Best_Score==M[i][j][0]):
         l_i = i      #store index in temperal variables
         l_j = j

  Alignments= [] #create an array for Alignments
  tot_aln = find_each_route(i,j) #return number of align paths
  aln_count = 0

  #Compiling alignments based on discovered matrix pathways
  for elem in Align_paths:
    i = l_i-1   
    j = l_j-1
    side_aln = '' 
    top_aln = ''
    step = 0
    aln_info = []
    for k in range(len(elem)):
        n_dir = elem[k]
        score = M[i+1][j+1][0]
        step = step + 1
        aln_info.append([step,score,n_dir])
        if n_dir == '2': # If diagonl
            side_aln = side_aln + Seq1[i]
            top_aln = top_aln + Seq2[j+1]
            i=i-1
            j=j-1
        elif n_dir == '1': # If up
            side_aln = side_aln + Gap_char
            top_aln = top_aln + Seq2[j+1]
            j=j-1
        elif n_dir == '3':  #If left
            side_aln = side_aln + Seq1[i]
            top_aln = top_aln + Gap_char
            i=i-1
    aln_count = aln_count + 1
    Alignments.append([top_aln,side_aln,elem,aln_info,aln_count])

  print('Total Alignments: ' + str(len(Alignments)))
  
  for elem in Alignments:
    print(elem[1][::-1]+'\n'+elem[0][::-1]+'\n') #print Alignments

"""Test Case"""

waterman("ACATAG","AATG")