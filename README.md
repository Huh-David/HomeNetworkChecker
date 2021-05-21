# HomeNetworkChecker
> To see who's at home.

This Python script makes use of the fritzconnection package by [kbr](https://github.com/kbr/fritzconnection/).
Furthermore the script takes a list of persons and the local ips of their mobile phones to check if they are currently at home or not.
If you are waiting for a person, you can just monitor one person until he/she gets home.

## Installation

First of all you have to clone the repository to your local pc (connected to a FritzBOX)
Then you have to install all used python packages as follows:

```sh
pip install -r requirements.txt
```

## Usage example

To use this script you have to find out all the ip addresses of your Fritz devices (FritzBOXs and FritzREPEATERs) and their passwords.
Also you have to search for the ips of specific persons (their mobile phone ip) you want to track. 
With the help of this information you can setup the script. 
More explanations are in the code.

## Development setup

## Release History

* 0.0.1
    * Work in progress

## Contributing

1. Fork it (<https://github.com/qt1337/HomeNetworkChecker/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
