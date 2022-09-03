2. Setting up a (new) project
============================
The whole **CARDmage** workflow was designed to be as intuitive and flexible as possible.
It doesn't require any coding skills at all and depends only on following a few but important
guidelines. But don't worry, this document should get you covered.

**Note:** To better understand this document it is advisable to download the source code
of this project, as the documentation explains pretty much everything based on the
*'testdata'* directory and its contents.


The TOML format
---------------
The entire configuration of the project itself and everything inside it is done in
**TOML files** (Toms Obvious, Minimal Language). Why this format? Because...

- of it's simple and clean overall structure.
- it requires only a minimal syntactical overhead (especially compared to XML).
- it is easy to read.
- it is easy to learn.

A TOML file basically consists of three different types of lines.

**Comments**::

    # This is a comment. Comments are mostly used for informational purposes or to deactivate
    # specific lines. Every hashtag symbol not included within quotes starts a comment in
    # that line – everything before that hashtag will be evaluated normally.

**Blocks**::

    [block]
    # The line above contains the definition tag of a new 'block'. It's purpose is to better
    # organize the files' contents. It acts very much like a folder on your desktop.
    # Every definition following a block tag is part of this block until another block tag opens
    # up a new block (and as such effectively closes the one before).

    [block.sub] # blocks may contain other blocks as well, just like a folder can contain subfolders

**Definitions**::

    title = "Example"
    # this is the most common type of line found in TOML files. It assigns the value "Example"
    # to the key 'title'. Later we can use this key to get back it's value, if needed.

    # IMPORTANT: Two keys cannot have the same name unless they belong to different blocks.

A valid line can only have one evaluated statement (either a block or a definition). It may
also contain an appended comment (since it will be ignored it doesn't count as a statement).

And that's all the magic to be found in TOML files.


The project settings
--------------------
If you want to create a new cardmage project, the **settings.toml** is the first file to start
with. This file tells the script where all the resources needed for creating the playing cards
are to be found. If you open up the **settings.toml** from the testdata directory you'll see
nothing but the paths to the different folders **relative** to the directory the
settings.toml is in.

For the sake of simplicity I separated the distinct parts of the test project into their
separate folders, but that's subject to ones' personal taste. You may want to rename the
folders, move some folders into other folders or throw everything into one folder
- as long as you remember to set the paths in the **settings.toml** accordingly everything
should work just as fine.

However be careful if you think about mixing project parts together in different folders or
creating a new folder for each card. *CARDmage* won't support such project setups as it would
introduce the requirement for a search algorithm and with that adds unnecessary levels of
complexity to the script.

Once the directories are in place and configured in the **settings.toml** you're ready to
start developing your own open source card game.

`Read on`_ for an in-depth explanation of how to configure the different aspects of your card
game.