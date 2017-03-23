import pickle
import os

import config
import testrunner
import utils

class Reinforcer:
    def __init__(self, suites):
        self.suites = suites
        self.alpha = config.get_alpha()

    def init_baselines(self, compilation, execution):
        cache_file = Reinforcer.__ethalon_file__("compilation", compilation)
        self.compilation = self.__load_cache__(cache_file)
        if not self.compilation:
            self.compilation = {}
            tests = testrunner.get_tests(self.suites, compilation)
            tests = testrunner.run(tests)

            for test in tests:
                self.compilation[str(test)] = test.compile_time
            self.__cache__(self.compilation, cache_file)

        cache_file = Reinforcer.__ethalon_file__("execution", execution)
        self.execution = self.__load_cache__(cache_file)
        if not self.execution:
            self.execution = {}
            if compilation != execution or not tests:
                tests = testrunner.get_tests(self.suites, execution)
                tests = testrunner.run(tests)

            for test in tests:
                self.execution[str(test)] = test.execution_time
            self.__cache__(self.execution, cache_file)

    def calculate_reward(self, test):
        C = self.compilation[str(test)]
        E = self.execution[str(test)]
        alpha = self.alpha
        Cp = test.compile_time
        Ep = test.execution_time
        if not Cp or not Ep: return -1
        return (E - Ep) / E + alpha * (C - Cp) / C

    def run(self):
        tests = testrunner.get_tests('-OW -ftrain-wazuhl')
        self.__check__(tests)
        while(True):
            result = testrunner.run_random(test)
            print "Result: ", self.calculate_reward(result)

    def __check__(self, tests):
        tests = set(map(str, tests))
        compilation_tests = set(self.compilation.keys())
        execution_tests = set(self.execution.keys())
        message = "Ethalon tests ({0}) differ from the ones for Wazuhl!"
        if tests != compilation_tests:
            utils.error(message.format("compilation"))
        if tests != execution_tests:
            utils.error(message.format("execution"))

    def __cache__(self, data, cache_file):
        with open(cache_file, 'w') as cache:
            pickle.dump(data, cache)

    def __load_cache__(self, cache_file):
        if not os.path.exists(cache_file):
            return None
        with open(cache_file, 'r') as cache:
            return pickle.load(cache)

    @staticmethod
    def __ethalon_file__(name, flags):
        return os.path.join(config.get_output(),
                            "{0}.{1}.ethalon".format(name, utils.pathify(flags)))
