from batch_transit_times import PandasWrapper
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def test_init():
    helper = PandasWrapper()
    assert helper

if __name__ == '__main__':
    logging.info('initializing tests.')
    test_init()
    logging.info('completed tests.')
