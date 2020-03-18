import numpy as np

filename=input('Enter the file name:')
match_score=input('Enter the match score:')
mis_match_score=input('Enter the mismatch score:')
gap_score=input('Enter the gap penalty:')

sequence_file=open(filename, 'r')
x=sequence_file.readlines()
seq1=x[0]
seq2=x[1]
n=len(seq1)+1
m=len(seq2)+1

match=int(match_score)
mis_match=int(mis_match_score)
gap=int(gap_score)

#creating the matrix
matrix = [ [ 0 for i in range(n-1) ] for j in range(m) ] 
matrix[0][0]=0


#initialize first row and column
for i in range(1,n-1):
  matrix[0][i]=0

for y in range(1,m):
  matrix[y][0]=0

#move matrix is for tracing the movements
move=[ [ 0 for i in range(n-1) ] for j in range(m) ]
align1=''
align2=''

#filling up the score matrix
for z in range(1,n-1):
  for t in range(1,m):
    if seq1[z-1]==seq2[t-1]:
      matrix[t][z]=max(0, matrix[t-1][z]+gap, matrix[t][z-1]+gap, matrix[t-1][z-1]+match) #filling up the score matrix
    else:
      matrix[t][z]=max(0, matrix[t-1][z]+gap, matrix[t][z-1]+gap, matrix[t-1][z-1]+mis_match)

    #filling up the movement matrix
    if matrix[t][z]==matrix[t][z-1]+gap:
      move[t][z]=3 #move vertically
    elif matrix[t][z]==matrix[t-1][z]+gap:
      move[t][z]=2 #move horizontal 
    elif matrix[t][z]==matrix[t-1][z-1]+match or matrix[t][z]==matrix[t-1][z-1]+mis_match:  #mark the movements to traceback
        move[t][z]=1 #move diagonal
    #elif matrix[t][z]==matrix[t-1][z]+gap:
     # move[t][z]=2 #move horizontal (yatay)
    #elif matrix[t][z]==matrix[t][z-1]+gap:
     # move[t][z]=3 #move vertically
    else:
      move[t][z]=0 #end of the trace


#find the maximum score and its indexes 
mm=np.matrix(matrix)  
ind = np.unravel_index(np.argmax(mm, axis=None), mm.shape)
#max score indexes:
xx=ind[0]
yy=ind[1]
max_score=matrix[xx][yy]

#print(xx)
#print(yy)


#if there is no local alignment, in other words there is no macth, I align the sequences as they all have gaps. 
if matrix[xx][yy]==0:
  align2=align2+seq2
  for o in range(len(seq2)):
    align1=align1+'-'
  for p in range(len(seq1)-1):
    align2=align2+'-'
  align1=align1+seq1
  align1=align1[0:-1]

#if there is match, from starting max score tracing back until find 0
while matrix[xx][yy]!=0:
  if move[xx][yy]==1:
    align1=align1+seq1[yy-1];
    align2=align2+seq2[xx-1];
    xx=xx-1
    yy=yy-1
    #print(xx,yy)
  elif move[xx][yy]==2:
    align1=align1+'-';
    align2=align2+seq2[xx-1];
    xx=xx-1
    #print(xx,yy)
  elif move[xx][yy]==3:
    align1=align1+seq1[yy-1]
    align2=align2+'-'
    yy=yy-1
    #print(xx,yy)

align1=align1[::-1]
align2=align2[::-1]

#this is for indicator
align_indicator=''
for k in range(len(align1)):
  if align1[k]=='-' or align2[k]=='-':
    align_indicator=align_indicator+' '
  elif align1[k]==align2[k]:
    align_indicator=align_indicator+'|'
  else:
    align_indicator=align_indicator+'.'


#for creating output file. 
for s in range(len(filename)):
  if filename[s]=='_':
    output=filename[:s]
outputname=output+'_output'+filename[10]+'.txt'
outputfile=open(outputname, 'w')
outputfile.write(seq1)
outputfile.write(seq2)
outputfile.write('\n\n')
outputfile.write(align1+'\n')
outputfile.write(align_indicator+'\n')
outputfile.write(align2)
outputfile.write('\n\n')
outputfile.write('Score='+str(max_score)+' for Match='+str(match)+',  Mismatch='+str(mis_match)+', Gap='+str(gap))
outputfile.close()