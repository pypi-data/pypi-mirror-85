import numpy as np

#Forward mode, automatic differentiation class

##############################################
######       Arithmetic Operators       ######
##############################################
class forwardAD:
	def __init__(self, val, der=1.0):
		self.val = val
		self.der = der

	#Overloaded addition
	def __add__(self, other):

		#For adding of the same class, add derivatives
		try:
			out_val = self.val + other.val
			out_der = self.der + other.der

		#For adding a float, keep derivative
		except AttributeError:
			out_val = self.val + other
			out_der = self.der

		return forwardAD(out_val, out_der)

	#Overloaded subtraction
	def __sub__(self, other):

		#For subtracting of the same class, subtract derivatives
		try:
			out_val = self.val - other.val
			out_der = self.der - other.der

		#For subtracting a float, keep derivative
		except AttributeError:
			out_val = self.val - other
			out_der = self.der

		return forwardAD(out_val, out_der)

	#Overloaded multiplication
	def __mul__(self, other):

		#For multiplying the same class, use product rule
		try:
			out_val = self.val * other.val
			out_der = self.der * other.val + self.val * other.der

		#For multiplying a float, multiply the value
		except AttributeError:
			out_val = self.val * other
			out_der = self.der * other

		return forwardAD(out_val, out_der)


	#Overloaded division
	def __truediv__(self, other):

		#For dividing the same class, use quotient rule
		try:
			out_val = self.val / other.val
			out_der = (self.der * other.val - self.val * other.der)/(other.val ** 2.0)

		#For dividing a float, divide the value
		except AttributeError:
			out_val = self.val / other
			out_der = self.der / other

		return forwardAD(out_val, out_der)

	#Overloaded power
	def __pow__(self, other):

		#For power to same class, use logarithmic differentiation
		try:
			out_val = self.val ** other.val
			out_der = (other.der * np.log(self.val) + other.val * (self.der / self.val)) * (self.val ** other.val)

		#For raising to a float, do power rule
		except AttributeError:
			out_val = self.val ** other
			out_der = self.der * other * self.val **(other - 1.0)

		return forwardAD(out_val, out_der)

	### Reversed Operations ###

	# Addition is commutative
	def __radd__(self, other):
		return self.__add__(other)

	# Reverse subtraction
	def __rsub__(self, other):

		#If another of same type, then reverse order of subtraction
		try:
			out_val = other.val - self.val
			out_der = other.der - self.der

		#If a float, then reverse order subtract
		except AttributeError:
			out_val = other - self.val
			out_der = -1.0 * self.der

		return forwardAD(out_val, out_der)

	#Multiplication is commutative
	def __rmul__(self, other):
		return self.__mul__(other)

	#Reverse division
	def __rtruediv__(self, other):
		#For dividing the same class, use reversed quotient rule
		try:
			out_val = other.val / self.val
			out_der = (other.der * self.val - other.val * self.der)/(self.val ** 2.0)

		#For dividing a float, take derivative of f**(-1) using power rule
		except AttributeError:
			out_val = other / self.val
			out_der = (-1.0) * other * self.der / (self.val**2.0)
		
		return forwardAD(out_val, out_der)

	#Reverse power
	def __rpow__(self, other):

		#If base is same class, do logarithmic differentiation
		try:
			out_val = other.val ** self.val
			out_der = (self.der * np.log(other.val) + self.val * (other.der / other.val)) * (other.val ** self.val)

		#If base is a float, then b^x derivative rule
		except AttributeError:
			out_val = other ** self.val
			out_der = other ** self.val * self.der * np.log(other)

		return forwardAD(out_val, out_der)


##############################################
######       Elementary Functions       ######
##############################################

#For getting an 'e'
class e(forwardAD):
	def __init__(self, val=np.exp(1), der=0.0):
		self.val = val
		self.der = der

#For getting a log, defaults to natural log
class log(forwardAD):
	def __init__(self, inputs, base = np.exp(1)):

		#For getting log of variable expression, log is derivative/val
		try:
			self.val = np.log(inputs.val)/np.log(base)
			self.der = inputs.der / inputs.val

		#For log of float, use numpy.log
		except AttributeError:
			self.val = np.log(inputs) / np.log(base)
			self.der = 0.0


#####  Trignometric Functions #####

#For getting a sine
class sin(forwardAD):
	def __init__(self, inputs):

		#For getting sine of variable expression, der = in.der * cos(in.val)
		try:
			self.val = np.sin(inputs.val)
			self.der = inputs.der * np.cos(inputs.val)

		#For sine of float, use numpy.sin
		except AttributeError:
			self.val = np.sin(inputs)
			self.der = 0.0


#For getting a cosine
class cos(forwardAD):
	def __init__(self, inputs):

		#For getting cosine of variable expression, der = -in.der * sin(in.val)
		try:
			self.val = np.cos(inputs.val)
			self.der = -inputs.der * np.sin(inputs.val)

		#For cosine of float, use numpy.cos
		except AttributeError:
			self.val = np.cos(inputs)
			self.der = 0.0


#For getting a tangent
class tan(forwardAD):
	def __init__(self, inputs):

		#For getting tangent of variable expression, der = in.der * (1 + tan(in.val)^2)
		try:
			self.val = np.tan(inputs.val)
			self.der = inputs.der * (1 + np.tan(inputs.val)**2)

		#For tanget of float, use numpy.tan
		except AttributeError:
			self.val = np.tan(inputs)
			self.der = 0.0


##### Inverse Trignometric Functions #####

#For getting a inverse sine
class arcsin(forwardAD):
	def __init__(self, inputs):

		#For getting arcsin of variable expression, der = in.der * (1/sqrt(1-inputs.val**2))
		try:
			self.val = np.arcsin(inputs.val)
			self.der = inputs.der * (1/np.sqrt(1-inputs.val**2))

		#For arcsin of float, use numpy.arcsin
		except AttributeError:
			self.val = np.arcsin(inputs)
			self.der = 0.0


#For getting a inverse cosine
class arccos(forwardAD):
	def __init__(self, inputs):

		#For getting arccos of variable expression, der = -in.der * sin(in.val)
		try:
			self.val = np.arccos(inputs.val)
			self.der = -inputs.der * (1/np.sqrt(1-inputs.val**2))

		#For arccos of float, use numpy.arccos
		except AttributeError:
			self.val = np.arccos(inputs)
			self.der = 0.0


#For getting a inverse tangent
class arctan(forwardAD):
	def __init__(self, inputs):

		#For getting arctan of variable expression, der = in.der * (1 / in.val^2)
		try:
			self.val = np.arctan(inputs.val)
			self.der = inputs.der * (1/(1+inputs.val**2))

		#For arctan of float, use numpy.arctan
		except AttributeError:
			self.val = np.arctan(inputs)
			self.der = 0.0


##### Hyperbolic Trignometric Functions #####

#For getting a hyperbolic sine
class sinh(forwardAD):
	def __init__(self, inputs):

		#For getting sinh of variable expression, der = in.der * sinh(in.val)
		try:
			self.val = np.sinh(inputs.val)
			self.der = np.cosh(inputs.val)

		#For sine of float, use numpy.tan
		except AttributeError:
			self.val = np.sinh(inputs)
			self.der = 0.0


#For getting a hyperbolic cosh
class cosh(forwardAD):
	def __init__(self, inputs):

		#For getting cosh of variable expression, der = in.der * sinh(in.val)
		try:
			self.val = np.cosh(inputs.val)
			self.der = np.sinh(inputs.val)

		#For sine of float, use numpy.cos
		except AttributeError:
			self.val = np.cosh(inputs)
			self.der = 0.0

#For getting a hyperbolic tangent
class tanh(forwardAD):
	def __init__(self, inputs):

		#For getting tangent of variable expression, der = in.der * (1 + tan(in.val)^2)
		try:
			self.val = np.tanh(inputs.val)
			self.der = inputs.der * (1 - np.tanh(inputs.val)**2)

		#For sine of float, use numpy.tan
		except AttributeError:
			self.val = np.tanh(inputs)
			self.der = 0.0

