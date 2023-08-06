import os
import pickle
from typing import Tuple

from netaddr.ip.sets import IPSet

from .providers import Providers


class WhichCloud:
    """
    >>> whichCloud = WhichCloud()
    >>> whichCloud.is('123.123.123.123')
    """

    def __init__(self):
        self.__aws_ips, self.__azure_ips, self.__gcp_ips = WhichCloud.__load_data()

    @staticmethod
    def __load_data() -> Tuple[IPSet, IPSet, IPSet]:
        pkg_dir = os.path.abspath(os.path.dirname(__file__))
        data_file = os.path.join(pkg_dir, "data", "data.pickle")
        with open(data_file, "rb") as f:
            aws_ips, azure_ips, gcp_ips = pickle.load(f)
            return aws_ips, azure_ips, gcp_ips

    def is(self, ip):
        if ip in self.__aws_ips:
            return Providers.AWS
        if ip in self.__azure_ips:
            return Providers.AZURE
        if ip in self.__gcp_ips:
            return Providers.GCP
        return None
