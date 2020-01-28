from random import randint
import random
from math import * 
import matplotlib.pyplot as plt
from copy import copy
mi=[[7,7],[7,8],[10,7],[10,8],[10,7.5],[7,7.5]]


"""
voir ici
https://medium.zenika.com/clusterings-in-machine-learning-k-means-and-k-medoids-examples-894f37db9350
"""

class Point:

	def __init__(self,x,y):
		self.point=(x,y)

	def getX(self):
		return self.point[0]

	def getY(self):
		return self.point[1]

	def getXY(self):
		return self.point

	def __str__(self):
		tmp="(x,y):({},{})".format(self.getX(),self.getY())
		return tmp

	def __eq__(self,others):
		if self.getX()==others.getX() and self.getY()==others.getY():
			return True
		else:
			return False

class Cluster:

	def __init__(self):
		self.listePoint=[]
		self.medoid=None
		

	def getliste(self):
		return self.listePoint

	def getCentre(self):
		return self.medoid

	def append(self,p):
		self.listePoint.append(p)

	def __str__(self):
		tmp0=""
		for i in self.getliste():
			tmp0+=str(i.getXY())+" "
		tmp="la liste est : {}\nle Centre {}".format(tmp0,self.medoid())
		return tmp

class Partie:

	def __init__(self,nbrCluster,nbrPoint):
		self.creeListePoint(nbrPoint)
		self.creeLesClusters(nbrCluster)
		self.DG=None
		self.nbrCluster=nbrCluster

	def creeListePoint(self,nbrPoint):
		self.listeDesPoints=[]
		li1=random.sample(range(50),nbrPoint)
		li2=copy(li1)
		random.shuffle(li2)
		print("1er",li1)
		print("2er",li2)
		for i in range(nbrPoint):
			"""
			x1=randint(0,5)
			y1=randint(0,5)
			x=randint(8,10)
			y=randint(8,10)
			"""
			
			self.listeDesPoints.append(Point(mi[i][0],mi[i][1]))
			#self.listeDesPoints.append(Point(x1,y1))
	def nettoyage(self):
		n=1
		for i in self.getLesPoints():
			for j in self.getLesPoints()[n:len(self.getLesPoints())]:
				if i==j:
					print(i)
					print(j)
					self.getLesPoints().remove(i)
				n+=1

	def creeLesClusters(self,nbrCluster):
		self.listeDesClusters=[]
		for i in range(nbrCluster):
			x=Cluster()
			self.listeDesClusters.append(x)

	def initClusters(self):
		ind=0
		for i in self.getLesClusters():
			i.append(self.getLesPoints()[ind])
			i.medoid=self.getLesPoints()[ind]
			ind+=1
	def assocPoint(self):
		dg=0
		for i in self.getLesPoints():
			x=float('inf')
			indcie=0
			bol=False
			for j in self.getLesClusters():
				if self.distanceEucl(i,j.getCentre())<x  :
					x=self.distanceEucl(i,j.getCentre())
					ind=indcie
					dg+=x
				indcie+=1
			for j in self.getLesClusters():
				if j.medoid==i:
					bol=True
			if bol == False:
				self.getLesClusters()[ind].append(i)
		self.DG=dg
	def assocPoint2(self,ind,med):
		dg=0
		for lm in self.getLesClusters():
			rec=lm.medoid
			lm=Cluster()
			lm.medoid=rec
			lm.append(rec)

		self.getLesClusters()[ind]=Cluster()
		self.getLesClusters()[ind].medoid=med

		self.getLesClusters()[ind].append(med)

		for i in self.getLesPoints():
			x=float('inf')
			indcie=0
			bol=False
			for j in self.getLesClusters():
				if self.distanceEucl(i,j.getCentre())<x  :
					x=self.distanceEucl(i,j.getCentre())
					ind=indcie
					dg+=x
				indcie+=1
			for j in self.getLesClusters():
				if j.medoid==i:
					bol=True
			if bol == False:
				self.getLesClusters()[ind].append(i)
		self.DG=dg

	def getDG(self):
		return self.DG



	def getLesPoints(self):
		return self.listeDesPoints

	def getLesClusters(self):
		return self.listeDesClusters

	def distanceEucl(self,g,p):
		x=sqrt(   (g.getX()-p.getX())**2  + (g.getY()-p.getY())**2  )
		return x

	def test(self):
		d=self.distanceEucl(self.getLesClusters()[0].medoid,self.getLesClusters()[0].getliste()[0])
		return d

	def run(self):
		condition=True
		while condition==True:
			condition=False
			indice=0
			for i in self.getLesClusters():
				for j in self.getLesPoints():
					x=True
					for k in self.getLesClusters():
						if j==k.medoid:
							x=False
					if x==True:
						oldm=i.medoid
						oldcl=i
						olddg=self.DG
						"""
						self.getLesClusters()[indice]=Cluster()
						self.getLesClusters()[indice].medoid=j
						self.getLesClusters()[indice].append(j)
						self.assocPoint2(indice,j)
						"""
						print(olddg,"||||",self.DG)
						if olddg-self.DG<=0:
							self.getLesClusters()[indice]=oldcl
							self.assocPoint2(indice,oldm)
							self.DG=olddg
						else:
							print("1")
							condition=True
				indice+=1


		
	def afficher(self):
		lix=[]
		liy=[]
		lix1=[]
		liy1=[]
		ind=1
		li=["x","o","*","+","s","_","|"]
		plt.subplot(2,1,1)
		for j in self.getLesClusters():
			for i in j.getliste():
				lix1.append(i.getX())
				liy1.append(i.getY())

		plt.scatter(lix1,liy1,s=15,c="#000000")
		plt.title("** Agrandir ou réduire la fenêtre pour mieux visualiser **\n\nFigure avant clustering")

		plt.subplot(2,1,2)
		for j in self.getLesClusters():
			for i in j.getliste():
				lix.append(i.getX())
				liy.append(i.getY())
			#plt.subplot(2,1,1)
			if lix!=[] and liy!=[]:
				x=randint(100000,999999)
				x="#"+str(x)+""
				y="Cluster "+str(ind)
				ind+=1
				plt.scatter(lix,liy,  c=x,s=50, label=y,marker=li[0])
				li.remove(li[0])
			lix=[]
			liy=[]
		
		plt.legend(bbox_to_anchor=(1.12, 1.05))
		plt.title("Figure après clustering")
		plt.show()


				 

				

	def __str__(self):
		kk=1
		tmp0=""
		for i in self.getLesPoints():
			tmp0+=str(i.getXY())+" "
		tmp0+="\n----------------------------------------------------"
		tmp1=""
		for j in self.getLesClusters():
			tmp2=""
			for k in j.getliste() :
				tmp2+=str(k.getXY())+" "
			tmp1+="- cluster "+str(kk)+" ["+tmp2+"]"+str(j.getCentre().getXY())+"\n"
			kk+=1

		tmp="-liste des Points crée {}\n-liste des Clusters \n{}".format(tmp0,tmp1)
		return tmp




#p1=Point(1,2)
#p2=Point(2,3)
#print(p1)
#print(p2)
#c1=Cluster()
#c1.append(p1)
#c1.append(p2)
#print(c1)
par=Partie(3,6)
#print(par)
par.initClusters()
#print(par)
par.assocPoint()
print(par.DG)
par.run()

#print(par.test())
print(par)
par.afficher()

















