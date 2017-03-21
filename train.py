#!/usr/bin/python

import sys
import os
from suites import suites
from src import options, config

def main():
    options.parse()
    print config.get_clang()
    print len(suites.get_suites())

if __name__ == "__main__":
    main()
