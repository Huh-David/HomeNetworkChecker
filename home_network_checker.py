import time
import itertools

from datetime import datetime
from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.core.exceptions import FritzServiceError
from win10toast import ToastNotifier

from sql_connection import sql_connection


def get_active_ips_of_fwlan(fwlan):
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


def notify_windows_toast(person):
    """
    Used to notify user directly in windows 10 if person gets home or so...
    :return:
    """
    toast = ToastNotifier()
    toast.show_toast(str(person) + ' at home',
                     str(person) + ' is finally at home.\nGo hug him/her!\nIt\'s ' + str(datetime.now()),
                     duration=5)
    print(str(person) + ' entered home at ' + str(datetime.now()))
    exit()


class HomeNetworkChecker:
    fwlans: [FritzWLAN] = []

    def __init__(self, fritz_logins, persons):
        """
        :param fritz_logins: ips of FritzBOXs and FritzREPEATERs with passwords
        :param persons: ips of persons with name
        """
        self.fritz_addresses = fritz_logins
        self.persons = persons
        self.tracking_period = 0
        self.seconds_until_terminate = 0

        # instantiate fwlans once in __init__ for improved performance
        self.instantiate_fwlans()

    def get_console_input(self):
        """
        Just dialog to setup how long the script should be run
        tracking_period: time between each check
        seconds_until_terminate: seconds until scripts ends
        :return: seconds_until_terminate, tracking_period
        """
        seconds_until_terminate = None
        while not type(seconds_until_terminate) == int:
            seconds_until_terminate = input('How long should the script be run in seconds?\n\'0\' for unlimited\n')
            try:
                seconds_until_terminate = int(seconds_until_terminate)
            except:
                pass

        tracking_period = None
        while not type(tracking_period) == int:
            tracking_period = input('How much time should be between each request?\n')
            try:
                tracking_period = int(tracking_period)
            except:
                pass

        self.seconds_until_terminate = seconds_until_terminate
        self.tracking_period = tracking_period

    def get_ips_from_fwlans(self) -> [str]:
        """
        Uses a list of FritzWLAN instances and returns a list of ip addresses from the active devices
        """
        device_ips: [str] = []

        for fwlan in self.fwlans:
            for ip in get_active_ips_of_fwlan(fwlan):
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
                persons_at_home.append((person, True))
            else:
                persons_at_home.append((person, False))

        return persons_at_home

    def instantiate_fwlans(self):
        """
        FritzWLAN instances should only be instantiated once to improve performance
        """
        for address in self.fritz_addresses:
            if len(address) > 2:
                self.fwlans.append(FritzWLAN(address=address[0], user=address[2], password=address[1]))
            else:
                self.fwlans.append(FritzWLAN(address=address[0], password=address[1]))

    def track_specific_person(self, delay=0):
        """
        Use this function to track one specific person until he or she gets home
        :param delay: delay in seconds until the script starts

        person: combination of ip and name as follows
        e.g. {'ip': '192.168.188.42', 'name': 'Mom'}

        :return: Notification in windows
        """
        # user input for length of script time
        self.get_console_input()

        counter = 0

        for ip, person in self.persons:
            print(str(counter) + '.', str(person))
            counter += 1

        person_index = int(input('\nWhich person do you want to track?\nGive me the number in front of the person\n'))

        person: {} = {
            'ip': self.persons[person_index][0],
            'name': self.persons[person_index][1]
        }

        time.sleep(delay)

        if self.seconds_until_terminate == 0:
            while True:
                ips = self.get_ips_from_fwlans()
                if person['ip'] in ips:
                    notify_windows_toast(person['name'])

                print('waiting for ' + str(person['name']))
                time.sleep(self.tracking_period)
        else:
            time_end = time.time() + self.seconds_until_terminate
            while time.time() < time_end:
                ips = self.get_ips_from_fwlans()
                if person['ip'] in ips:
                    notify_windows_toast(person['name'])

                print('waiting for ' + str(person['name']))
                time.sleep(self.tracking_period)

    def monitor_home_network(self):
        """
        Monitor active devices for x seconds
        :return: returns nothing but prints list of persons with boolean
        """
        # user input for length of script time
        self.get_console_input()

        if self.seconds_until_terminate == 0:
            while True:
                print(self.get_persons_at_home())
                time.sleep(self.tracking_period)
        else:
            time_end = time.time() + self.seconds_until_terminate
            while time.time() < time_end:
                print(self.get_persons_at_home())
                time.sleep(self.tracking_period)

    def monitor_home_network_once_and_save_to_db(self):
        """
        !!! Setup sql.ini properly and create the required table before with sql_connection.create_table()

        Monitor active devices only once and saves result to database
        :return: returns nothing but saves list of persons with boolean to database
        """

        mariadb_connection = sql_connection()
        # mariadb_connection.create_table()

        mariadb_connection.save_to_database(self.get_persons_at_home())
