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
                            env=configuration_env, stdout=devnull, stderr=devnull)
        print "Configuration is finished"

        self.__init_tests__()

    def __init_tests__(self):
        utils.check_executable('lit')
        lit = subprocess.Popen(['lit', '--show-tests', '.'], stdout=subprocess.PIPE)
        output = lit.stdout.read()
        pattern = r'test-suite :: (.*)'
        results = re.findall(pattern, output)
        self.tests = [Test(os.path.join(self.build, test), self) for test in results]
        self.tests = [test for test in self.tests if "Benchmark" in test.path]

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
        with open(os.devnull, 'wb') as devnull:
            subprocess.call(['make', '-j5', self.name], stdout=devnull, stderr=devnull)

    def run(self):
        test_run = subprocess.Popen(['lit', self.path], stdout=subprocess.PIPE)
        output = test_run.stdout.read()
        compile_pattern = r'compile_time: (.*)'
        execution_pattern = r'exec_time: (.*)'
        compile_time = re.search(compile_pattern, output)
        if compile_time: compile_time = float(compile_time.group(1))
        execution_time = re.search(execution_pattern, output)
        if execution_time: execution_time = float(execution_time.group(1))
        self.compile_time, self.execution_time = compile_time, execution_time

    def __str__(self):
        return self.name
