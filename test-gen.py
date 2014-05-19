#!/usr/bin/env python
# XFAIL: *
import logging
import random
import os
import sys

min = 0
max = 1024

def gen_test(seed, directory, testNumber):
    if not os.path.isdir(directory):
        logging.error('{} is not a directory'.format(directory))
        sys.exit(1)
    source="""\
# RUN: python %s > %t
# RUN: %diff %s.expect %t
"""
    expectString = ""
    random.seed(seed)
    for n in range(0,100):
        line='FOO ' + hex(random.randint(0, sys.maxsize))
        source += "print('{}')\n".format(line)
        expectString += line + '\n'

    # Write test
    path = os.path.join(directory, 'test-{}.py').format(testNumber)
    logging.debug('Writing to {}'.format(path))
    with open(path,'w+') as f:
        f.write(source)

    # Write expected output
    path += '.expect'
    logging.debug('Writing to {}'.format(path))
    with open(path, 'w+') as f:
        f.write(expectString)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    for dirnum in range(0,10):
        dirpath = os.path.join( os.path.abspath(os.getcwd()), 'testdir-{}'.format(dirnum))
        logging.debug('Creating directory "{}"'.format(dirpath))
        os.mkdir(dirpath)

        # Generate tests
        for testnum in range(0,100):
            gen_test(testnum + dirnum, dirpath, testnum)
