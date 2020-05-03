import string

def dist(s,t):
	sLen=len(s)
	tLen=len(t)
	arr=[[0 for i in range(sLen+1)] for j in range (tLen+1)]
	print(s[0])

	for i in range(tLen+1):
		for j in range(sLen+1):
			if i==0:
				arr[i][j]=j
			if j==0:
				arr[i][j]=i
	#print(arr)
	for j in range(0,sLen):
		for i in range(0,tLen):
			if t[i]==s[j]:
				cost=0
			else:
				cost=1
			#print(cost)
			#print(i,j,cost)
			arr[i+1][j+1] = min(1+arr[i][j+1],1+arr[i+1][j], cost + arr[i][j])
	return arr[sLen][tLen]

def normalize(s):
	return s.translate(str.maketrans('', '', string.punctuation)).lower()

print(normalize("a.ss."))