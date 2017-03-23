#!/usr/bin/python

import random
import sys
import os
from suites import suites
from src import options, config

def main():
    options.parse()
    for suite in suites.get_suites():
        suite.configure(config.get_clang(), config.get_clangpp(), '-OW', '-OW')
        tests = suite.get_tests()
        print "Wazuhl has {0} tests for training".format(len(tests))
        for x in xrange(50):
            test = random.choice(tests)
            print "Running test '{0}'".format(test)
            test.compile()
            test.run()
            print "Results: {0}, {1}".format(test.compile_time, test.execution_time)

if __name__ == "__main__":
    main()
