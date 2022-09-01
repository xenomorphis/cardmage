Setting up a (new) project
==========================
The whole **CARDmage** workflow was designed to be as intuitive and flexible as possible.
It doesn't require any coding skills at all and depends only on following a few but important
guidelines. But don't worry, this document should get you covered.

**Note:** To better understand this document it is advisable to download the source code
of this project, as it explains pretty much everything based on the *'testdata'*
directory and its contents.


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