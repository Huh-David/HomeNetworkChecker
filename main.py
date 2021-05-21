from configparser import ConfigParser
from person_checker import PersonChecker


def config_list_parser(config_string):
    """
    Takes list from config as config_string
    :returns config as list
    """

    return_config = []
    config_string = config_string[1:-1].replace('\n', '').split(',')

    for config_part in config_string:
        return_config.append(config_part[1:-1].replace('\'', '').split(':'))

    return return_config


if __name__ == '__main__':
    # Load the configuration file
    config = ConfigParser()
    config.read('config.ini')

    # Parse lists in config to real lists

    # persons from whom you know the ip and want to track
    # rather choose the ips of mobile phones because these should be a good indicator
    persons = config_list_parser(config.get("persons", "known_ips"))

    # in case you have multiple fritzrepeater you need to add them all
    fritzrepeaters = config_list_parser(config.get("fritzrepeaters", "addresses"))

    p_checker = PersonChecker(fritz_addresses=fritzrepeaters, persons=persons, tracking_period=5)
    p_checker.monitor_home_network(seconds_until_terminate=5)
