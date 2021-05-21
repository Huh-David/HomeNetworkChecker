from person_checker import HomeNetworkChecker
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


def main():
    # On first start or if files are missing the write_json() methods will be executed
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
                    'Then go ahead and change the settings in write_json()! \nOr create the required files yourself... :(')
                exit()
            else:
                print('No valid input\n')

    seconds_until_terminate = None
    while not type(seconds_until_terminate) == int:
        seconds_until_terminate = input('How long should the script be run in seconds?\n')
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

    # persons from whom you know the ip and want to track
    # rather choose the ips of mobile phones because these should be a good indicator if somebody is at home
    persons_json = read_json('persons.json')

    # in case you have multiple fritzrepeaters you need to add them all
    fritz_logins_json = read_json('fritz_logins.json')

    persons: [[]] = []
    fritz_logins: [[]] = []

    for x in persons_json['known_ips']:
        persons.append([x['ip'], x['name']])

    for x in fritz_logins_json['fritz_logins']:
        fritz_logins.append([x['ip'], x['password']])

    home_network_checker = HomeNetworkChecker(fritz_logins=fritz_logins,
                                              persons=persons,
                                              tracking_period=tracking_period)
    print('Initialized HomeNetworkChecker')
    home_network_checker.monitor_home_network(seconds_until_terminate=seconds_until_terminate)


if __name__ == '__main__':
    main()
