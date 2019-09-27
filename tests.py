from fedex_config import CONFIG_OBJ
from batch_transit_times import PandasWrapper
import logging
import sys
import os
import pandas as pd


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def test_init():
    helper = PandasWrapper(CONFIG_OBJ, partition_size=0, storage_dir=None)
    assert helper

def test_batch():
    root_dir = os.path.dirname(os.path.abspath(__name__))
    df = pd.read_csv(os.path.join(root_dir, 'testing_data.csv'))
    assert not df.empty

    # 7981 -> 07981
    df.origin_zip = df.origin_zip.astype('str').str.zfill(5)
    df.dest_zip = df.dest_zip.astype('str').str.zfill(5)

    storage_dir = os.path.join(root_dir, 'instance')
    helper = PandasWrapper(CONFIG_OBJ, partition_size=2,
        storage_dir=storage_dir)
    helper.df = df.copy()
    assert not helper.df.empty

    helper.run()
    assert 'transit_time' in helper.df.columns

    logging.info('transit_times: %s' % helper.df.transit_time)

if __name__ == '__main__':
    logging.info('initializing tests.')
    test_init()
    test_batch()
    logging.info('completed tests.')
