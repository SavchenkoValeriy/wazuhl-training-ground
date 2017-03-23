import config
import random

def get_tests(suites, flags):
    tests = []
    for suite in suites:
        suite.configure(config.get_clang(), config.get_clangpp(), flags, flags)
        tests.extend(suite.get_tests())
    return tests

def run(tests):
    for test in tests:
        run_test(test)
    return tests

def run_random(tests):
    test = random.pick(tests)
    return run_test(test)

def run_test(test):
    test.compile()
    test.run()
    return test
