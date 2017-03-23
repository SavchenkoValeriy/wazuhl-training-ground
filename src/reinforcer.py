import config
import testrunner

class Reinforcer:
    def __init__(self, suites):
        self.suites = suites
        self.alpha = config.get_alpha()

    def init_baselines(self, compilation, execution):
        self.compilation = {}
        tests = testrunner.get_tests(self.suites, compilation)
        tests = testrunner.run(tests)

        for test in tests:
            self.compilation[str(test)] = test.compile_time

        self.execution = {}
        if compilation != execution:
            tests = testrunner.get_tests(self.suites, execution)
            tests = testrunner.run(tests)

        for test in tests:
            self.execution[str(test)] = test.execution_time

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
        while(True):
            result = testrunner.run_random(test)
            print "Result: ", self.calculate_reward(result)
