import os
from optparse import OptionParser
import config
import utils

def parse():
    usage = "usage: %prog [options] [wazuhl installation directory]"
    version = "0.0.1a"
    parser = OptionParser(usage, version=version)

    parser.add_option('-o', '--output-directory',
                      type='string',
                      action='store',
                      dest='output',
                      default='train.out',
                      help='Directory to store training files')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        utils.error("Please, specify path to Wazuhl installation")

    installation = args[0]
    utils.check_file(installation)
    config.set_wd(installation)
    config.set_output(options.output)
