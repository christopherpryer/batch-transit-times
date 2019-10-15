from fedex.services.availability_commitment_service import \
    FedexAvailabilityCommitmentRequest
from fedex.tools.conversion import sobject_to_dict
from .transit_time_types import transit_time_types
import pandas as pd
import numpy as np
import logging
import traceback
import os
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class FedexHelper:
    def __init__(self, config, partition_size, storage_dir):
        self.df = pd.DataFrame()
        self.config = config
        self.partition_size = partition_size
        self.storage_dir = storage_dir

    def get_transit_time(self, origin_zip, origin_country, dest_zip,
        dest_country):
        self.request = FedexAvailabilityCommitmentRequest(self.config)
        self.request.Origin.PostalCode = origin_zip
        self.request.Origin.CountryCode = origin_country
        self.request.Destination.PostalCode = dest_zip
        self.request.Destination.CountryCode = dest_country
        self.request.Service = 'FEDEX_GROUND'

        try:
            self.request.send_request()
            response_dict = sobject_to_dict(self.request.response)
            # output display formatting
            origin_str = '%s, %s' % (
                self.request.Origin.PostalCode,
                self.request.Origin.CountryCode)
            destination_str = '%s, %s' % (
                self.request.Destination.PostalCode,
                self.request.Destination.CountryCode)

            logging.info('origin: %s' % origin_str)
            logging.info('destination: %s' % destination_str)
            for option in response_dict['Options']:
                if option['Service'] == 'FEDEX_GROUND':
                    logging.info('TransitTime: %s' % option['TransitTime'])
                    return option['TransitTime'] # TODO: convert from type to int
                else:
                    logging.warning('No Fedex Ground Service found.')
                    return np.nan
        except Exception as e:
            logging.warning('Fedex request failed. Error: %s' % e)
            return np.nan
            #traceback.print_exc() # for initial dev TODO: create debug mode


    def manage_partitioning(self, partition_number):
        if not self.df.empty:
            start = self.start_i
            end = start + self.partition_size
            partition = self.df[start:end].copy()

            transit_times = []
            for i in range(len(partition)):
                o_zip = partition.origin_zip.iloc[i]
                o_country = partition.origin_country.iloc[i]
                d_zip = partition.dest_zip.iloc[i]
                d_country = partition.dest_country.iloc[i]
                tt = self.get_transit_time(
                    origin_zip=o_zip,
                    origin_country=o_country,
                    dest_zip=d_zip,
                    dest_country=d_country)

                if pd.isnull(tt):
                    transit_times.append(tt)
                else:
                    transit_times.append(transit_time_types[tt])

            partition['transit_time'] = transit_times
            filename = 'partition_%s.csv' % partition_number
            filepath = os.path.join(self.storage_dir, filename)
            logging.info('Saving %s to %s' % (partition.shape, filepath))
            partition.to_csv(filepath, index=False)
            self.start_i += self.partition_size
            return transit_times

    def run(self):
        self.start_i = 0
        n_partitions = int(np.ceil(len(self.df)/self.partition_size))
        transit_times = []
        for i in range(n_partitions):
            transit_times += self.manage_partitioning(i)
        self.df['transit_time'] = transit_times
