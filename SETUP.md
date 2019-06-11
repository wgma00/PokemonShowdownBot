Setting up
---------
The following are the necessary dependencies for running this software.

### Operating System:
- APT/RPM based Linux distribution like Debian or Fedora
- Some functionality may still work on Windows and MacOS, but have not been fully tested. Use at your own discretion.
- If you're not running Linux natively then consider running this project in [vagrant](https://www.vagrantup.com/); more info provided below.

### LaTeX:
- Requires the following to be installed, ``texlive`` and ``poppler-utils``

### Calculator:
- Requires that ``gcalccmd`` is installed

#### Python:
- Python 3.4+. No plans are made to make this support earlier versions.
- [PIP](https://pip.pypa.io/en/stable/). Package manager for python

#### Guide:
0. (optional) Setting up an environment separate from your host OS or global python interpreter to avoid dependency conflicts. 

- If you're on Linux you might find setting up a virtualenv with the following ``virtualenv -p /usr/bin/python3 quadbot && source quadbot/bin/activate`` will be helpful. 
- If you're on MacOS or Windows setting up [vagrant](https://www.vagrantup.com/docs/installation/) will be useful. Then you can use ``vagrant init && vagrant ssh`` to load this project's production environment. 

1. Clone the git repo to your desired location
2. Run ``git update-index --assume-unchanged plugins/SecretCommands.py`` to stop tracking SecretCommands.py
3. Install pip dependencies manually  with `pip install -r requirements.txt`, and install the aforementioned software manually. 
   Or you run the install script using  ``chmod +x install.sh && ./install.sh``
4. Follow the instructions in `details-example.yaml` to configure your bot for login
5. Run using `python3 app.py`
6. (optional) Test for errors you can run ``test.sh`` using ``chmod +x test.sh && ./test.sh``


License
-------

This project is distributed under the terms of the [GPLv3 and MIT License][1].

  [1]: https://github.com/wgma00/quadbot/blob/master/NOTICE

Credits
-------

Maintainer

- wgma00 
