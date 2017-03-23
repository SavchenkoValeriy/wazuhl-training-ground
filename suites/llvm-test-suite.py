import os
import re
import shutil
import subprocess
from src import config, utils

class Suite:
    name = "llvm-test-suite"
    def __init__(self):
        self.tests = []

    def get_tests(self):
        return self.tests

    def configure(self, CC, CXX, COPTS, CXXOPTS):
        output = config.get_output()
        suite = os.path.join(output, self.name)

        self.build = os.path.join(output, self.name + "-build")
        if os.path.exists(self.build):
            shutil.rmtree(self.build)
        os.makedirs(self.build)
        self.go_to_builddir()

        configuration_env = os.environ.copy()
        configuration_env['CC'] = CC
        configuration_env['CXX'] = CXX

        with open(os.devnull, 'wb') as devnull:
            subprocess.call(['cmake', suite,
                             '-DCMAKE_BUILD_TYPE=Release',
                             '-DCMAKE_C_FLAGS_RELEASE={0}'.format(COPTS),
                             '-DCMAKE_CXX_FLAGS_RELEASE={0}'.format(CXXOPTS)],
                            env=configuration_env)
        print "Configuration is finished"

        self.__init_tests__()

    def __init_tests__(self):
        utils.check_executable('lit')
        lit = subprocess.Popen(['lit', '--show-tests', '.'], stdout=subprocess.PIPE)
        output = lit.stdout.read()
        pattern = r'test-suite :: (.*)'
        results = re.findall(pattern, output)
        self.tests = [Test(os.path.join(self.build, test), self) for test in results]

    def go_to_builddir(self):
        os.chdir(self.build)

class Test:
    def __init__(self, path, suite):
        self.path = path
        self.name = Test.__get_test_name__(path)
        self.suite = suite

    @staticmethod
    def __get_test_name__(path):
        _, test_file = os.path.split(path)
        test, _ = os.path.splitext(test_file)
        return test

    def compile(self):
        self.suite.go_to_builddir()
        subprocess.call(['make', '-j5', self.name])

    def run(self):
        subprocess.call(['lit', self.path])
