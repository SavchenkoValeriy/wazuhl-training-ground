import imp
import inspect
import os
import sys
import utils

def get_suites():
    return [x.Suite() for x in suite_modules]

def load_suites():
    modules = []
    for suite, suite_file in get_suite_files():
        candidate = imp.load_source(suite, suite_file)
        if looks_like_suite(candidate):
            check_suite(candidate)
            modules.append(candidate)
    return modules

def looks_like_suite(module):
    classes_in_module = [i[0] for i in inspect.getmembers(module, inspect.isclass)]
    return "Suite" in classes_in_module and "Test" in classes_in_module

def check_suite(suite):
    check_suite_class(suite.Suite)
    check_test_class(suite.Test)

def check_suite_class(suite):
    check_name(suite)
    check_get_tests(suite)
    check_configure(suite)

def check_test_class(test):
    check_compile(test)
    check_run(test)

def check_name(suite):
    if not hasattr(suite, "name"):
        utils.error("Suite should have a name! Please, define a member variable in class")

def check_get_tests(suite):
    check_method(suite, "get_tests", 1)

def check_configure(suite):
    check_method(suite, "configure", 5)

def check_compile(test):
    check_method(test, "compile", 1)

def check_run(test):
    check_method(test, "run", 1)

def check_method(class_object, name, number_of_args):
    class_name = class_object.__name__
    predicate = lambda(x) : inspect.ismethod(x) and x.__name__ == name
    matching_functions = inspect.getmembers(class_object, predicate)
    if len(matching_functions) != 1:
        utils.error("'{0}' class must have '{1}' method!".format(class_name, name))
    spec = inspect.getargspec(matching_functions[0][1])
    if len(spec.args) != number_of_args:
        utils.error("'{1}' method of '{0}' class must have exactly {2} arguments!".
                    format(class_name, name, number_of_args))

def get_suite_files():
    directory = get_suites_dir()
    return [(os.path.splitext(suite)[0], os.path.join(directory, suite))
            for suite in os.listdir(directory)
            if suite != "suites.py" and suite.endswith(".py")]


def get_suites_dir():
    return os.path.dirname(os.path.realpath(__file__))

suite_modules = load_suites()
