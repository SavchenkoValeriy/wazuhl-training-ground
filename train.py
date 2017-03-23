#!/usr/bin/python

import sys
import os
from suites import suites
from src import options, config

def main():
    options.parse()
    for suite in suites.get_suites():
        suite.configure(config.get_clang(), config.get_clangpp(), '-OW', '-OW -ftrain-wazuhl')
        tests = suite.get_tests()
        for test in tests:
            test.compile()
            test.run()

if __name__ == "__main__":
    main()
