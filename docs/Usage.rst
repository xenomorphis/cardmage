5. Installation & usage of the command line tool
================================================
Once you've configured everything the last step is getting CARDmage to do it's job and render
the cards. Since CARDmage is a command line tool written in Python you'll have a bunch of
dependencies to take care of first.

5.1 Installation
----------------

Install 'python'
''''''''''''''''
The first step is getting the necessary compilers set up on your machine. You'll find the
correct installation package (version 3.10 or higher) for your OS on the official
`python website <https://www.python.org/downloads/>`_.

If you're on Linux there's a chance that the python packages are already shipped with your
distro (to be sure check it via the command line with ``python --version`` or ``python3.10 --version``
– if you get back a version number you're fine). If not you'll need to install ``python`` first.

- On Debian/APT-based distibutions: ``sudo apt install python3.10``
- On ArchLinux and it's derivatives: ``pacman -S python``

As usual check if you're able to use python via the command line as described above before you
proceed to the next step.

Install 'ImageMagick'
'''''''''''''''''''''
Since CARDmage is only a kind of a translation layer between your configuration files and ImageMagick
you'll need ImageMagick as well. ImageMagick is an open-source image editing tool that will
do all of the heavy lifting for us in the background.

- For Windows I'll stick to the *don't repeat yourself* principle and link you to a nice `installation guide <https://docs.wand-py.org/en/0.6.10/guide/install.html#install-imagemagick-on-windows>`_ instead of writing one myself.
- For Linux the world's once again a bit easier: ``sudo apt-get install libmagickwand-dev`` for Debian/APT, ``pacman -S imagemagick`` for Arch and ``yum install ImageMagick-devel`` for Fedora/CentOS.
- For Mac you'll need homebrew to do ``brew install imagemagick`` or MacPorts for ``sudo port install imagemagick``.

Install 'pip'
'''''''''''''
**pip** is an acronym for *Package Installer for Python* and the de-facto standard package
manager for everything python-related. With ``pip`` setting up the necessary dependencies for
CARDmage is a breeze.

- Windows & MacOS: pip is already included if you've installed Python in version 3.4 or higher from the python.org website
- Linux: ``sudo apt install pip`` (Debian/APT) or ``pacman -S python-pip`` (Arch-a-likes)

Check the availability of pip with the following command: ``pip --version``. If you get back
a version number you can proceed with the next step.

Install dependencies
''''''''''''''''''''
Now you've pip up and running you can easily install the needed dependencies via *pip*::

    pip install toml
    pip install Wand

5.2 How to use CARDmage
-----------------------
Once you've everything set up, you can start to work with CARDmage to build your cards.
Just download the ``cardmage.py`` found in the release section and copy that file into the
project directory (the same folder the ``settings.toml`` is in). Now open a terminal window
in the same folder:

- On Windows: Enter ``cmd`` into the address bar of the file browser while being inside the folder
- On Linux distributions using *Dolphin* as their file browser: Right-click into an empty space inside the folder and choose the *Open Terminal here* option from the menu.

Inside the terminal you can now execute the script with ``py cardmage.py`` on Windows or
``python cardmage.py`` on Linux.

CLI syntax
''''''''''
Inside the terminal you can now execute the script using the following syntax::

    [py|python] cardmage.py [-Options] [Card file(s)]

    Options:
        -h  Displays more information about how to use the script
        -p  Activates print quality mode

    Examples:
        python cardmage.py
            renders all card files found inside the 'cards' directory

        python cardmage.py -p B_Aetheriumschmiede.toml
            renders only the card file named 'B_Aetheriumschmiede.toml' in print mode

    Note:
        Depending on your OS you'll need to call the script either with 'py' or 'python'

Once the script has finished you'll find a new *dist* folder in the project directory
containing your freshly built cards in PNG format.