class Suite:
    name = "llvm-test-suite"
    def __init__(self):
        self.tests = []

    def get_tests(self):
        return self.tests

    def configure(self, CC, CXX, COPTS, CXXOPTS):
        pass

class Test:
    def __init__(self, name, directory):
        pass

    def compile(self):
        pass

    def run(self):
        pass
