#!/usr/bin/python

import sys
import os
from suites import suites

def main():
    print len(suites.get_suites())

if __name__ == "__main__":
    main()
