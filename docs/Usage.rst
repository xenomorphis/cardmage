5. Usage of the command line tool
=================================
Once you've configured everything the last step is getting CARDmage to do it's job and render
the cards. Since CARDmage is a command line tool written in Python you'll have a bunch of
dependencies to take care of first.

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