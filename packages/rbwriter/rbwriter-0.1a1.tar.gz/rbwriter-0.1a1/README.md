# Report Booklet Writer

[![CodeFactor](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer/badge)](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/LICENSE)

Never write a report booklet on your own again, Report Booklet Writer does it for you!



## Installation

```bash
# First clone the project
git clone https://github.com/TheCoder777/Report-Booklet-Writer.git

# Change directory
cd Report-Booklet-Writer

# Install requirements
pip install -r requirements.txt

# Finally run it
python server.py
```

The program will mostly take care of itself during the checkup, so there's need to worry!




## Usage

If you load it up, go to [localhost:8000](localhost:8000) (current default) and either click on 'create account', or click the quickedit icon on sidebar (try to hover for a little bit!)

You can either download the single PDFs in edit mode, or export all to one PDF in the overview tab!

It's as easy as that!




## Users

Every account has a nickname that can be changed in the settings (it's pretty useless right now, but you'll use this to login later!)

You Email needs to be in a `name@provider.domain` format

Your password needs to have 8 characters, one capital letter, one number and one special character.

Feel annoyed? Well at least it's for security...




## Configuration

You can configure all settings via the web interface on /settings or by clicking on the settings icon in the sidebar!

Do me a favor and be careful with some settings like `start week` and `start year`, this often gets easily messed up.



If you like the extreme, or you just want to mess around, you may also edit the `defines/configs.py` file. (Do this on your own risk!)

You'll be notified if everything went the correct way when you click the save button!

To reset the configuration, just click the reset button! (This is to reset the values you put in since the last refresh)

The 'reset to default button' will hard reset your configuration to absolute defaults, with **no chance to restore your data**, so please be careful with that!




## Debugging

You can easily debug the project by using a --debug/-d flag when running:

```bash
python server.py --debug
```



## Todo

- Mail server (just wait for it, you'll see)
- Private/Public Profile setting
- all TODOs in the code (`# TODO: ...`)



## License

The project is licensed under the MIT license.



------

This project follows these guidelines for:

- [Code of Conduct](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CODE_OF_CONDUCT.md) 
- [Contributing](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CONTRIBUTING.md) 



Current maintainer and owner: [TheCoder777](https://github.com/thecoder777)
