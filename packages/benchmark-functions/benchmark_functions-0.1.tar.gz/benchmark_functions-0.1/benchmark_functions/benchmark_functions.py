#!/usr/bin/env python3

import math
import numpy as np
import logging
from . import functions_info_loader as fil

functions_info = fil.FunctionsInfo()

class _BenchmarkFunction(object):
	def __init__(self, name, n_dimensions=2, opposite=False):
		if type(n_dimensions)!=int or n_dimensions==0:
			raise ValueError("Functions can be created only using a number of dimensions greater than 0.")
		self.name=name
		self.opposite=opposite
		self.n_dimensions=n_dimensions
		self.parameters=[]

	def __call__(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate(point)
		else:
			return self._evaluate(point)
	
	def derivative(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate_derivative(point)
		else:
			return self._evaluate_derivative(point)
	
	def second_derivative(self, point, validate=True):
		if validate:
			self._validate_point(point)
		if self.opposite:
			return - self._evaluate_second_derivative(point)
		else:
			return self._evaluate_second_derivative(point)

	def _validate_point(self, point):
		if type(point)!=tuple and type(point)!=list:
			raise ValueError("Functions can be evaluated only on tuple or lists of values, found "+str(type(point)))
		if len(point)!=self.n_dimensions:
			raise ValueError("Function "+self.name+" declared as defined for "+str(self.n_dimensions)+" dimensions, asked to be evaluated on a point of "+str(len(point))+" dimensions")
		if not all(type(v)==float or type(v)==int or type(v)==np.float64 for v in point):
			idx=None
			for i in range(len(point)):
				t=type(point[i])
				if t!=float and t!=int:
					idx=i
					break
			vs=[x for x in point]
			vs[idx]=str(vs[idx])+"("+str(type(vs[idx]))+")"
			raise ValueError("Functions can only be evaluated on float or int values, passed "+str(vs))
	
	def _evaluate(self, point):
		raise NotImplementedError("Function "+self.name+" is not defined.")
	def _evaluate_derivative(self, point):
		raise NotImplementedError("Derivative of function "+self.name+" is not defined.")
	def _evaluate_second_derivative(self, point):
		raise NotImplementedError("Second derivative of function "+self.name+" is not defined.")
	
	def getName(self):
		return self.name

	def getMinima(self):
		if self.opposite:
			return [(self(v), v) for v in functions_info.get_maxima(self.name, self.n_dimensions, self.parameters)]
		else:
			return [(self(v), v) for v in functions_info.get_minima(self.name, self.n_dimensions, self.parameters)]
	# return a tuple (value, position)
	def getMinimum(self):
		minima = self.getMinima()
		if len(minima)==0:
			return None
		pos=0
		for i in range(len(minima))[1:]:
			if minima[i][0]<minima[pos][0]:
				pos=i
		return minima[pos]

	def getMaxima(self):
		if self.opposite:
			return [(self(v), v) for v in functions_info.get_minima(self.name, self.n_dimensions, self.parameters)]
		else:
			return [(self(v), v) for v in functions_info.get_maxima(self.name, self.n_dimensions, self.parameters)]
	# return a tuple (value, position)
	def getMaximum(self):
		maxima = self.getMaxima()
		if len(maxima)==0:
			return None
		pos=0
		for i in range(len(maxima))[1:]:
			if maxima[i][0]>maxima[pos][0]:
				pos=i
		return maxima[pos]

	def getSuggestedBounds(self):
		b=functions_info.get_suggested_bounds(self.name, self.parameters)
		return ([b[0]]*self.n_dimensions, [b[1]]*self.n_dimensions)

	def show(self, asHeatMap=False):
		if self.n_dimensions>2:
			raise ValueError(f"Only functions defined in 1 or 2 dimensions can be visualised (N={self.n_dimensions})")
		if self.n_dimensions==1 and asHeatMap:
			raise ValueError(f"Only functions defined in 2 dimensions can be visualised as heatmap (N={self.n_dimensions})")
		try:
			import matplotlib.pyplot as plt
		except ImportError:
			logging.error("In order to show the function the matplotlib module is required.")
			return
		bounds_lower, bounds_upper=self.getSuggestedBounds()

		x = np.linspace(bounds_lower[0], bounds_upper[0], 50)
		if self.n_dimensions>1:
			y = np.linspace(bounds_lower[1], bounds_upper[1], 50)

			X, Y = np.meshgrid(x, y)
			Z = np.asarray([[self((X[i][j],Y[i][j])) for j in range(len(X[i]))] for i in range(len(X))])
		
		fig = plt.figure()
		fig.canvas.set_window_title('Benchmark Function: '+self.name)
		fig.suptitle(self.name)
		if asHeatMap:
			plt.contour(x,y,Z,15,linewidths=0.5,colors='k') # hight lines
			plt.contourf(x,y,Z,15,cmap=plt.cm.rainbow, vmax=Z.max(), vmin=Z.min()) # heat map
			plt.xlabel('x')
			plt.ylabel('y')
			cbar = plt.colorbar()
			cbar.set_label('z')
		elif self.n_dimensions==1:
			y = np.asarray([self([v]) for v in x])
			plt.xlabel('x')
			plt.ylabel('y')
			plt.plot(x,y)
		else:	
			ax = plt.axes(projection='3d')
			ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
			ax.view_init(60, 35)
			ax.set_zlabel('z')
			ax.set_xlabel('x')
			ax.set_ylabel('y')
		plt.show()

'''
Continuous, convex and unimodal.
'''
class Hypersphere(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Hypersphere", n_dimensions, opposite)

	def _evaluate(self,point):
		ret = sum([pow(x,2) for x in point])
		return ret
	def _evaluate_derivative(self, point):
		return sum([2.0*x for x in point])
	def _evaluate_second_derivative(self, point):
		return 2.0*len(point)

class Hyperellipsoid(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Hyperellipsoid", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([pow(i,i) + pow(point[i],2) for i in range(len(point))])
		return ret
	def _evaluate_derivative(self, point):
		return sum([2.0*point[i] for i in range(len(point))])
	def _evaluate_second_derivative(self, point):
		return 2.0*len(point)

'''
Continuous, non-convex and multimodal.
'''
class Rosenbrock(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Rosenbrock", n_dimensions, opposite)
	def _evaluate(self,point):
		s=0.0
		for i in range(len(point)-1):
			s+=100*pow(point[i+1] - pow(point[i],2),2) + pow(1.0-point[i],2)
		return s

'''
Continuous, non-convex and (highly) multimodal. 
Location of the minima are regularly distributed.
'''
class Rastrigin(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Rastrigin", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([pow(p,2) - 10.0*math.cos(2.0*math.pi*p) for p in point]) + 10.0*len(point)
		return ret
	def _evaluate_derivative(self, point):
		return sum([2.0*p + 20.0*math.pi*math.sin(2.0*math.pi*p) for p in point])
	def _evaluate_second_derivative(self, point):
		return sum([2.0 + 40.0*pow(math.pi,2)*math.cos(2.0*math.pi*p) for p in point])

'''
Continuous, non-convex and (highly) multimodal. 
Location of the minima are geometrical distant.
'''
class Schwefel(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Schwefel", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([-p*math.sin(math.sqrt(abs(p))) for p in point])
		return ret
	def _evaluate_derivative(self, point):
		if point==[0.0]*len(point):
			return 0.0
		else:
			return sum([-pow(p,2)*math.cos(math.sqrt(abs(p)))/(2.0*pow(abs(p),3.0/2.0)) - math.sin(math.sqrt(abs(p))) for p in point if p!=0.0])

'''
Continuous, non-convex and (highly) multimodal. 
The suggested behaviour is zoom-dependent: 
	- [zoom=0] general overview [-600<= x_i <= 600] suggests convex function;
	- [zoom=1] medium-scale view [-10 <= x_i <= 10] suggests existence of local optima;
	- [zoom=2] zoom on the details [-5 <= x_i <= 5] reveal complex structure of numerous local optima;
'''

class Griewank(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, zoom=0, opposite=False):
		if zoom not in [0,1,2]:
			raise ValueError("Griewank function defined with a zoom level not in [0,1,2]")
		super().__init__("Griewank", n_dimensions, opposite)
		self.parameters=[("zoom",zoom)]
	def getName(self):
		return "Griewank"
	def _evaluate(self,point):
		part1=0.0
		part2=1.0
		for i in range(len(point)):
			part1+=pow(point[i],2)
			part2*=math.cos(point[i]/math.sqrt(i+1))
		ret = 1.0 + part1/4000.0 - part2
		return ret

'''
Continuous, non-convex and multimodal.
Clear global minimum at the center surrounded by many symmetrical local minima.
'''
class Ackley(_BenchmarkFunction):
	def __init__(self, n_dimensions=2,a=20,	b=.2,	c=2.0*math.pi, opposite=False):
		super().__init__("Ackley", n_dimensions, opposite)
		self.a=a
		self.b=b
		self.c=c
	def _evaluate(self,point):
		part1=0.0
		part2=0.0
		for i in range(len(point)):
			part1+=pow(point[i],2)
			part2+=math.cos(self.c*point[i])
		ret = -self.a * math.exp(-self.b * math.sqrt(part1/len(point))) - math.exp(part2/len(point)) + self.a + math.exp(1.0)	
		return ret
'''
Continuous, non-convex and (highly) multimodal. 
Contains n! local minimum. 
'''
class Michalewicz(_BenchmarkFunction):
	def __init__(self, n_dimensions=2,m=10, opposite=False):
		super().__init__("Michalewicz", n_dimensions, opposite)
		self.m=m
	def _evaluate(self,point):
		s=0.0
		for i in range(len(point)):
			s+=math.sin(point[i])*pow(math.sin((i+1)*pow(point[i],2)/math.pi),2*self.m)
		return -s # it's not an error

'''
Non-convex, contains multiple asymmetrical local optima
'''
class EggHolder(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Egg Holder", n_dimensions, opposite)
	def _evaluate(self,point):
		s=0.0
		for i in range(len(point)-1):
			s+=(point[i+1]+47)*math.sin(math.sqrt(abs(point[i+1]+47.0+point[i]/2.0))) + point[i]*math.sin(math.sqrt(abs(point[i] - (point[i+1] + 47.0))))
		return -s
'''
Mutlimodal function with local optima regions of different depths
'''
class Keane(_BenchmarkFunction):
	def __init__(self,n_dimensions=2, opposite=False):
		super().__init__("Keane", n_dimensions, opposite)
	# validate the point according the Keane's function conditions
	def validate(self,point):
		p=1.0
		for x in point:
			p*=x
		if 0.75>p:
			raise ValueError("Product condiction violated on the Keane's function ("+str(0.75)+'>'+str(p)+")")
		if sum(point)> 7.5*len(point):
			raise ValueError("Sum condiction violated on the Keane's function ("+str(7.5*len(point))+'<'+str(sum(point))+")")

	def _evaluate(self,point):
		# try:
		# 	self.validate(point)
		# except ValueError:
		# 	return 0.0 # might want to propagate instead
		if sum(point)==0: # this is a more forgiving condition
			return 0.0
		part0=1.0
		for x in point:
			part0*=pow(math.cos(x),2)
		part1=abs(sum([pow(math.cos(x),4) for x in point]) - 2.0*part0)
		part2=math.sqrt(sum([(i+1)*pow(point[i],2) for i in range(len(point))]))
		return -part1/part2

'''
Highly multimodal symmetric function 
'''
class Rana(_BenchmarkFunction):
	def __init__(self,n_dimensions=2, opposite=False):
		super().__init__("Rana", n_dimensions, opposite)
	def _evaluate(self,point):
		s=0.0
		for i in range(len(point)-1):
			p1=point[i]*math.cos(math.sqrt(abs(point[i+1]+point[i]+1.0)))
			p2=math.sin(math.sqrt(abs(point[i+1]-point[i]+1.0)))
			p3=(1.0+point[i+1])*math.sin(math.sqrt(abs(point[i+1]+point[i]+1.0)))
			p4=math.cos(math.sqrt(abs(point[i+1]-point[i]+1.0)))
			s+=p1*p2 + p3*p4
		return s

'''
Continuous, unimodal, mostly a plateau with global minimum in a small central area.
It's defined only for 2 dimensions.
'''
class Easom(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Easom", 2, opposite)
	def _evaluate(self,point):
		ret = -math.cos(point[0])*math.cos(point[1])*math.exp(-pow(point[0]-math.pi,2)-pow(point[1]-math.pi,2))
		return ret

'''
Multimodal, "stairs"-like function, with multiple plateau at different levels
'''
class DeJong3(_BenchmarkFunction):
	def __init__(self,n_dimensions=2, opposite=False):
		super().__init__("De Jong 3", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([math.floor(x) for x in point])
		return ret
'''
Continuous, multimodal, multiple symmetric local optima with narrow basins on a plateau
It's defined only for 2 dimensions.
'''
class DeJong5(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("De Jong 5", 2, opposite)
		self.A=[[-32, -16,  0,  16,  32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32], 
						[-32, -32, -32,-32, -32, -16, -16, -16, -16, -16, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32]]
	def _evaluate(self,point):
		ret = pow(0.002 + sum([1.0/(i + 1.0 + pow(point[0] - self.A[0][i],6) + pow(point[1] - self.A[1][i],6)) for i in range(25)]),-1)
		return ret

'''
Continuous, multimodal with an asymmetrical hight slope and global minimum on a plateau.
It's defined only for 2 dimensions.
'''
class GoldsteinAndPrice(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Goldstein and Price", 2, opposite)
	def _evaluate(self,point):
		a = 1.0 + pow(point[0]+point[1]+1.0,2)*(19.0-14.0*point[0]+3.0*pow(point[0],2)-14.0*point[1]+6.0*point[0]*point[1]+3.0*pow(point[1],2))
		b = 30.0 + pow(2*point[0]-3.0*point[1],2)*(18.0-32.0*point[0]+12.0*pow(point[0],2)+48.0*point[1]-36.0*point[0]*point[1]+27.0*pow(point[1],2))
		return a*b

'''
(logaritmic variant of Goldstein and Price) continuous, with multiple asymmetrical slopes and global minimum near local optima.
It's defined only for 2 dimensions.
'''
class PichenyGoldsteinAndPrice(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Picheny, Goldstein and Price", 2, opposite)
	def _evaluate(self,point):
		x1= 4.0*point[0]-2.0
		x2= 4.0*point[1]-2.0
		a = 1.0 + pow(x1+x2+1.0,2)*(19.0-14.0*x1+3.0*pow(x1,2)-14.0*x2 + 6.0*x1*x2+3.0*pow(x2,2))
		b = 30.0 + pow(2*x1-3.0*x2,2)*(18.0-32.0*x1+12.0*pow(x1,2)+48.0*x2-36.0*x1*x2+27.0*pow(x2,2))
		ret = 1.0/2.427 * (math.log(a*b) - 8.693)
		return ret

'''
continuous, multimodal, with optima displaced in a symmetric way.
'''
class StyblinskiTang(_BenchmarkFunction):
	def __init__(self, n_dimensions=2, opposite=False):
		super().__init__("Styblinski and Tang", n_dimensions, opposite)
	def _evaluate(self,point):
		ret = sum([pow(x,4) - 16.0*pow(x,2) + 5.0*x for x in point])/2.0
		return ret

'''
Continuous, unimodal, uneven slopes on the sides
It's defined only for 2 dimensions.
'''
class McCormick(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("McCormick", 2, opposite)
	def _evaluate(self,point):
		ret = math.sin(point[0]+point[1]) + pow(point[0]-point[1],2) - 1.5*point[0] + 2.5*point[1] +1.0
		return ret


class MartinGaddy(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Martin and Gaddy", 2, opposite)
	def _evaluate(self,point):
		ret = pow(point[0] - point[1],2) + pow((point[0] + point[1] - 10.0)/3.0,2) 
		return ret

class Schaffer(_BenchmarkFunction):
	def __init__(self, opposite=False):
		super().__init__("Schaffer", 2, opposite)
	def _evaluate(self,point):
		tmp=pow(point[0],2) + pow(point[1],2)
		ret = 0.5 + (pow(math.sin(math.sqrt(tmp)),2) - 0.5)/pow(1.0 + 0.001*tmp,2)
		return ret

# class Shekel(_BenchmarkFunction):
# 	def __init__(self,n_dimensions,m=10, opposite=False):
# 		super().__init__("Shekel", n_dimensions, opposite)
# 		self.parameters=[('m',m)]
# 		self.m=m
# 		if n_dimensions==2:
# 			self.c=(0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5)
# 			self.A=[[-32, -16,  0,  16,  32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32], 
# 							[-32, -32, -32,-32, -32, -16, -16, -16, -16, -16, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32]]
# 		elif n_dimensions==4:
# 			self.c=(0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5)
# 			self.A=[[4,4,4,4],[1,1,1,1],[8,8,8,8],[6,6,6,6],[3,7,3,7],[2,9,2,9],[5,5,3,3],[8,1,8,1],[6,2,6,2],[7,3.6,7,3.6]]
# 		elif n_dimensions==10:
# 			self.c=(0.806, 0.517, 0.10, 0.908, 0.965, 0.669, 0.524, 0.902, 0.531, 0.876, 0.462,
# 							0.491, 0.463, 0.714, 0.352, 0.869, 0.813, 0.811, 0.828, 0.964, 0.789,
# 							0.360, 0.369, 0.992, 0.332, 0.817, 0.632, 0.883, 0.608, 0.326)
# 			self.A=[[9.681,0.667,4.783,9.095,3.517,9.325,6.544,0.211,5.122,2.020],
# 							[9.400,2.041,3.788,7.931,2.882,2.672,3.568,1.284,7.033,7.374],
# 							[8.025,9.152,5.114,7.621,4.564,4.711,2.996,6.126,0.734,4.982],
# 							[2.196,0.415,5.649,6.979,9.510,9.166,6.304,6.054,9.377,1.426],
# 							[8.074,8.777,3.467,1.863,6.708,6.349,4.534,0.276,7.633,1.567],
# 							[7.650,5.658,0.720,2.764,3.278,5.283,7.474,6.274,1.409,8.208],
# 							[1.256,3.605,8.623,6.905,0.584,8.133,6.071,6.888,4.187,5.448],
# 							[8.314,2.261,4.224,1.781,4.124,0.932,8.129,8.658,1.208,5.762],
# 							[0.226,8.858,1.420,0.945,1.622,4.698,6.228,9.096,0.972,7.637],
# 							[305,2.228,1.242,5.928,9.133,1.826,4.060,5.204,8.713,8.247],
# 							[0.652,7.027,0.508,4.876,8.807,4.632,5.808,6.937,3.291,7.016],
# 							[2.699,3.516,5.874,4.119,4.461,7.496,8.817,0.690,6.593,9.789],
# 							[8.327,3.897,2.017,9.570,9.825,1.150,1.395,3.885,6.354,0.109],
# 							[2.132,7.006,7.136,2.641,1.882,5.943,7.273,7.691,2.880,0.564],
# 							[4.707,5.579,4.080,0.581,9.698,8.542,8.077,8.515,9.231,4.670],
# 							[8.304,7.559,8.567,0.322,7.128,8.392,1.472,8.524,2.277,7.826],
# 							[8.632,4.409,4.832,5.768,7.050,6.715,1.711,4.323,4.405,4.591],
# 							[4.887,9.112,0.170,8.967,9.693,9.867,7.508,7.770,8.382,6.740],
# 							[2.440,6.686,4.299,1.007,7.008,1.427,9.398,8.480,9.950,1.675],
# 							[6.306,8.583,6.084,1.138,4.350,3.134,7.853,6.061,7.457,2.258],
# 							[0.652,2.343,1.370,0.821,1.310,1.063,0.689,8.819,8.833,9.070],
# 							[5.558,1.272,5.756,9.857,2.279,2.764,1.284,1.677,1.244,1.234],
# 							[3.352,7.549,9.817,9.437,8.687,4.167,2.570,6.540,0.228,0.027],
# 							[8.798,0.880,2.370,0.168,1.701,3.680,1.231,2.390,2.499,0.064],
# 							[1.460,8.057,1.336,7.217,7.914,3.615,9.981,9.198,5.292,1.224],
# 							[0.432,8.645,8.774,0.249,8.081,7.461,4.416,0.652,4.002,4.644],
# 							[0.679,2.800,5.523,3.049,2.968,7.225,6.730,4.199,9.614,9.229],
# 							[4.263,1.074,7.286,5.599,8.291,5.200,9.214,8.272,4.398,4.506],
# 							[9.496,4.830,3.150,8.270,5.079,1.231,5.731,9.494,1.883,9.732],
# 							[4.138,2.562,2.532,9.661,5.611,5.500,6.886,2.341,9.699,6.500]]
# 		else:
# 			raise ValueError("The Shekel function is only defined for 2,4 or 10 dimensions")
# 	def _evaluate(self,point):
# 		return sum([pow(self.c[i] + sum([pow(point[j] - self.A[j][i],2) for j in range(self.n_dimensions)]),-1) for i in range(self.m)])
# 		n_dimensions=len(point)
# 		if n_dimensions==2:
# 			s=sum([pow(j + pow(point[0] - self.A[0][j],9) + pow(point[1] - self.A[1][j],6),-1) for j in range(24)]) # in the formal equation it should be ^6 in both cases, instead it works only if it's ^9 and ^6
# 			ret = pow(1.0/500.0 + s,-1)
# 		elif n_dimensions==4:
# 			ret = -sum([pow(sum([pow(point[j] - self.A[i][j],2) for j in range(self.n_dimensions)]) + self.c[i],-1) for i in range(self.m)])
# 		elif n_dimensions==10:
# 			ret = sum([pow(sum([pow(point[j] - self.A[i][j],2) for j in range(self.n_dimensions)]) + self.c[i],-1) for i in range(30)])
# 		else:
# 			raise ValueError("The Shekel function is only defined for 2,4 or 10 dimensions")
# 		return ret

