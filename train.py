#!/usr/bin/python

import random
import sys
import os
from suites import suites
from src import options, config
from src.reinforcer import Reinforcer

def main():
    options.parse()
    reinforcer = Reinforcer(suites.get_suites())
    reinforcer.init_baselines('-O2', '-O2')
    reinforcer.run()

if __name__ == "__main__":
    main()
