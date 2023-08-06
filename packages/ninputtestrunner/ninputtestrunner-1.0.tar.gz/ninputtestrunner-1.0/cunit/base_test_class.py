import unittest
import inspect
import importlib
from   parameterized_test import ParameterizedTest
from   fast_fail import fail_fast_check
import os


class BaseTestClass():

	"""
	The main idea of this class is
	1) Load all the test suites/classes
	2) Run all the test methods

	"""

	test_file_path = []


	@staticmethod
	def test_case_loader(param, run_once, iteration_num = None, fail_fast = None):

		"""
			param: paramter to pass
			run_once: Boolean which can be used to skip tests. If True this will skip tests
			iteration_num: integer which can be used to pass iteration information to each unit tests

			Loads classes based on the module supplied.
		"""


		if "FAILFAST" in os.environ:
			fail_fast = os.environ['FAILFAST']


		if "RESUME" in os.environ:
			print (iteration_num)
			# If the current iteration is less than
			if iteration_num < int(os.environ['RESUME']):
				return

		if "STOP" in os.environ:
			# In case of end, we can successfully terminate the test runner
			if iteration_num > int(os.environ['STOP']):
				exit(0)


		# All test classes
		all_test_modules = BaseTestClass.test_file_path

		# List of Test cases
		list_test_cases = []

		# iterate over specific module in either client or server
		for specific_module in all_test_modules:

				module = importlib.import_module(specific_module)

				for name, obj in inspect.getmembers(module):
					# We look for only test classes with the name that starts with Test
					if inspect.isclass(obj):

						if name.startswith('Test'):
							test_class_name = obj
							list_test_cases.append(test_class_name)


		suite = unittest.TestSuite()

		# Only run test cases once.
		# TODO: My design decision to skip test cases is done in parameterized unit tests. Other option would be provide decorator but it didn't work well for me.



		# We have a parameterized test class, which passes parameters to each test case.
		for test_class_name in list_test_cases:

			BaseTestClass.skip_run_once(suite, run_once)
			suite.addTest(ParameterizedTest.parametrize(test_class_name, param=param))

		result = unittest.TextTestRunner(verbosity=2).run(suite)

		# Fail-early. This is important for external tool like CI to detect failures early and report it to developer

		if fail_fast:
			if not result.wasSuccessful():
				raise Exception('Functional test failure!')

		# Fail fast for Performance analysis

		if fail_fast:
			if fail_fast_check():
				raise Exception('Performance issue identified!')

	@staticmethod
	def skip_run_once(suite, run_once):


		"""

		Single run feature dependent on the input state i.e., at which iteration of input we should skip the tests from executing

		:param suite:
		:param run_once:
		:return:
		"""

		if run_once:

			list = open("test/test_run_once.lst").read().splitlines()

			for test_suite in suite.__iter__():
				for t in test_suite.__iter__():
					for run_once_test in list:
						if t.id().endswith( run_once_test) : # To skip `test_spam` and `test_ham`
							setattr(t, 'setUp', lambda: t.skipTest(' --- single run'))
							break


	@staticmethod
	def dicover_test_path(path):
		import os
		files = []
		# r=root, d=directories, f = files
		for r, d, f in os.walk(path):
			for file in f:
				if file.startswith("test_") and (file.endswith('.py') or file.endswith('.py.inst')):
					if file.endswith('.py.inst'):
						path = os.path.join(r, file).replace('/', '.').replace('.py.inst', '')
					elif file.endswith('.py'):
						path = os.path.join(r, file).replace('/', '.').replace('.py', '')
					path_index = path.rindex('test.')
					path = path[path_index:]

					files.append(path)

		BaseTestClass.test_file_path = files

