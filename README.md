# python-transit-times
Python package that leverages python-fedex to process ground transit times for shipment data.

### Instructions
Getting Fedex Ground transit times using FedexHelper helper:


```python
from batch_transit_times import FedexHelper
from fedex.config import FedexConfig


CONFIG_OBJ = FedexConfig(key='********',
                         password='********',
                         account_number='********',
                         meter_number='********',
                         freight_account_number='********',
                         use_test_server=True)


dir_path = 'path/to/directory'

# see testing_data.csv for required field names
df = pd.read_csv(os.path.join(root_dir, 'filename.csv'))

# pad zip codes if necessary: 7981 -> '07981'
df.origin_zip = df.origin_zip.astype('str').str.zfill(5)
df.dest_zip = df.dest_zip.astype('str').str.zfill(5)

# path to directory to store response partitions
storage_dir = os.path.join(root_dir, 'instance')

helper = FedexHelper(CONFIG_OBJ, partition_size=2,
    storage_dir=storage_dir)
helper.df = df.copy()

helper.run()

data_with_transit_times = helper.df.copy()
```
