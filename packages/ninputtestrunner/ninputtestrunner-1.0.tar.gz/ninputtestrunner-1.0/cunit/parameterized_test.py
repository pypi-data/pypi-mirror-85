import unittest

"""
	Since, there is no easy way to parametrized unit tests from outside.
	We use a technique for parametrizing test cases based creating a new subclass
	that extends unittest class. The parameterized class simply adds arguments in 
	the constructor	
"""

class ParameterizedTest(unittest.TestCase):

	""" TestCase classes that want to be parametrized should
		inherit from this class.
	"""

	def __init__(self, methodName='runTest', param=None):

		super(ParameterizedTest, self).__init__(methodName)
		self.param = param

	@staticmethod
	def parametrize(testcase_klass, param=None):

		""" Create a suite containing all tests taken from the given
			subclass, passing them the parameter 'param'.
		"""

		testloader = unittest.TestLoader()

		testnames = testloader.getTestCaseNames(testcase_klass)

		suite = unittest.TestSuite()

		for name in testnames:

			suite.addTest(testcase_klass(name, param=param))

		return suite


