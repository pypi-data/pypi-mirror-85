class AutoDiffToy:
	def __init__(self, val, der=1):
		self.val = val
		self.der = der

	def __add__(self, other):
		try:
			out_val = self.val + other.val
			out_der = self.der + other.der
			return AutoDiffToy(out_val, out_der)
		except AttributeError:
			try:
				out_val = self.val + other
				out_der = self.der
				return AutoDiffToy(out_val, out_der)
			except AttributeError:
				out_val = self + other.val
				out_der = other.der
				return AutoDiffToy(out_val, out_der)

	def __mul__(self, other):
		try:
			out_val = self.val * other.val
			out_der = self.der * other.val + self.val * other.der
			return AutoDiffToy(out_val, out_der)
		except AttributeError:
			try:
				out_val = self.val * other
				out_der = self.der * other
				return AutoDiffToy(out_val, out_der)
			except AttributeError:
				out_val = self * other.val
				out_der = self * other.der
				return AutoDiffToy(out_val, out_der)

	# These functions take care of commutativity
	def __radd__(self, other):
		return self.__add__(other)

	def __rmul__(self, other):
		return self.__mul__(other)