from fedex.services.availability_commitment_service import \
    FedexAvailabilityCommitmentRequest
from fedex.tools.conversion import sobject_to_dict
import pandas as pd
import numpy as np
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class PandasWrapper:
    def __init__(self, config):
        self.df = pd.DataFrame()
        self.config = config

    def get_transit_time(self, origin_zip, origin_country, dest_zip,
        dest_country):
        self.request = FedexAvailabilityCommitmentRequest(self.config)
        self.request.Origin.PostalCode = origin_zip
        self.request.Origin.CountryCode = origin_country
        self.request.Destination.PostalCode = dest_zip
        self.request.Destination.CountryCode = dest_country
        self.request.Service = 'FEDEX_GROUND'

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

    def run(self):
        if not self.df.empty:
            transit_times = []
            for i in range(len(self.df)):
                o_zip = self.df.origin_zip.iloc[i]
                o_country = self.df.origin_country.iloc[i]
                d_zip = self.df.dest_zip.iloc[i]
                d_country = self.df.dest_country.iloc[i]
                tt = self.get_transit_time(
                    origin_zip=o_zip,
                    origin_country=o_country,
                    dest_zip=d_zip,
                    dest_country=d_country)
                transit_times.append(tt)
            self.df['transit_time'] = transit_times
