import time
import itertools

from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.core.exceptions import FritzServiceError


class HomeNetworkChecker:
    fwlans: [FritzWLAN] = []

    def __init__(self, fritz_logins, persons, tracking_period):
        """
        :param fritz_logins: ips of FritzBOXs and FritzREPEATERs with passwords
        :param persons: ips of persons with name
        :param tracking_period: time between each check
        """
        self.fritz_addresses = fritz_logins
        self.persons = persons
        self.tracking_period = tracking_period

    def get_active_ips(self, fwlan):
        """
        Gets a FritzWLAN instance and returns a list of ip addresses from the active devices
        """
        active_ips = list()
        ip_addresses = []
        # iterate over all wlans:
        for n in itertools.count(1):
            fwlan.service = n
            try:
                hosts_info = fwlan.get_hosts_info()
            except FritzServiceError:
                break
            else:
                active_ips.extend(entry['ip'] for entry in hosts_info)

        for ip in active_ips:
            if len(ip) > 1:
                ip_addresses.append(ip)

        return active_ips

    def get_ips_from_fwlans(self) -> [str]:
        """
        Uses a list of FritzWLAN instances and returns a list of ip addresses from the active devices
        """
        device_ips: [str] = []

        for fwlan in self.fwlans:
            for ip in self.get_active_ips(fwlan):
                device_ips.append(ip)

        return device_ips

    def get_persons_at_home(self) -> [str]:
        """
        Uses a list of persons and active device ips to check if person is at home
        """
        ips = self.get_ips_from_fwlans()

        persons_at_home = []
        for ip, person in self.persons:
            if ip in ips:
                persons_at_home.append([person, True])
            else:
                persons_at_home.append([person, False])

        return persons_at_home

    def instantiate_fritzwlans(self):
        """
        FritzWLAN instances should only be instantiated once to improve performance
        """
        for address, password in self.fritz_addresses:
            self.fwlans.append(FritzWLAN(address=address, password=password))

    def monitor_home_network(self, seconds_until_terminate):
        """
        Monitor active devices for x seconds
        :param seconds_until_terminate: seconds until monitoring stops
        :return: returns nothing but prints list of persons with boolean
        """
        self.instantiate_fritzwlans()

        time_end = time.time() + seconds_until_terminate
        while time.time() < time_end:
            print(self.get_persons_at_home())
            time.sleep(self.tracking_period)
