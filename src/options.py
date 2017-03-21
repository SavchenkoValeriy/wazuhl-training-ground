import config
from optparse import OptionParser

def parse():
    usage = "usage: %prog [options]"
    version = "0.0.1a"
    parser = OptionParser(usage, version=version)

    parser.add_option('-w', '--wazuhl-directory',
                      type='string',
                      action='store',
                      dest='wd',
                      help='Wazuhl installation directory')

    (options, args) = parser.parse_args()
    config.set_wd(options.wd)
