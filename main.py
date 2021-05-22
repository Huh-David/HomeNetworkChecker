from home_network_checker import HomeNetworkChecker
import json
import os


def write_json():
    """
    On the initial start you will be asked to add some basic configuration for the program to work.
    If there are changes in configuration, just delete existing persons.json and fritz_logins.json.

    for example:

        FILENAME: persons.json
        'known_ips': [
            {'ip': '192.168.188.42', 'name': 'Person A'},
            {'ip': '192.168.188.69', 'name': 'Person B'}
        ]

        FILENAME: fritz_logins.json
        'fritz_logins': [
            {'ip': '192.168.188.1', 'password': 'password'},
            {'ip': '192.168.188.2', 'password': 'password'},
        ]

    """
    known_ips = {
        'known_ips': [
            {'ip': '192.168.188.42', 'name': 'Person A'},
            {'ip': '192.168.188.69', 'name': 'Person B'}
        ]
    }

    addresses = {
        'fritz_logins': [
            {'ip': '192.168.188.1', 'password': 'password'},
            {'ip': '192.168.188.2', 'password': 'password'},
        ]
    }

    with open('persons.json', 'w') as f:
        json.dump(known_ips, f, indent=4)

    with open('fritz_logins.json', 'w') as f:
        json.dump(addresses, f, indent=4)


def read_json(filename):
    """
    Gets a filename and returns content of file as json
    :param filename: file to read
    :return: content of file as json
    """
    f = open(filename)
    json_content = json.load(f)
    f.close()
    return json_content


def check_config_files():
    """
    # On first start or if files are missing the write_json() methods will / can be executed
    """
    if not os.path.isfile('persons.json') or not os.path.isfile('fritz_logins.json'):
        print('Some configuration files are missing.\nShould they be created automatically?')
        while True:
            create_automatically = input('Y/N\n')
            if create_automatically == "y" or create_automatically == "Y":
                print('The required files are being generated right now...')
                write_json()
                print('Files have been created')
                break
            elif create_automatically == "n" or create_automatically == "N":
                print(
                    'Then go ahead and change the settings in the write_json() method!\n'
                    'Or create the required files yourself... :(')
                exit()
            else:
                print('No valid input\n')


def main():
    """
    This method will be executed by default
    :return: List of all given persons with indicator if person is at home or not
    """
    check_config_files()  # checks if files are missing

    # persons from whom you know the ip and want to track
    # rather choose the ips of mobile phones because these should be a good indicator if somebody is at home
    persons_json = read_json('persons.json')
    persons: [[]] = []

    for x in persons_json['known_ips']:
        persons.append([x['ip'], x['name']])

    # in case you have multiple fritzrepeaters you need to add them all
    fritz_logins_json = read_json('fritz_logins.json')
    fritz_logins: [[]] = []

    for x in fritz_logins_json['fritz_logins']:
        fritz_logins.append([x['ip'], x['password']])

    home_network_checker = HomeNetworkChecker(fritz_logins=fritz_logins,
                                              persons=persons)
    print('Initialized HomeNetworkChecker')
    home_network_checker.monitor_home_network()
    # home_network_checker.track_specific_person()


if __name__ == '__main__':
    main()
