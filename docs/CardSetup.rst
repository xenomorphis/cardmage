3. How to build your own card game - Assets configuration
=========================================================
Now that you've told CARDmage where to find the assets needed for generating the cards, you
should now focus on the cards itself. CARDmage uses six different configurations (or parts)
to create your cards - but don't worry, a few of them are reusable once configured so you
don't need to redo most of it again and again for each card.

3.1 Images
----------
The image part is possibly the easiest one. Take a look into the *images* subfolder and you
won't see any TOML configuration here. That's because by the time the designers or artists
start creating some artworks the whole configuration part needed for placing the artworks on
the card is already done.

TL;DR: Nothing to do here.

3.2 Icons
---------
Icons bear similarities to the images described above. Just throw them all into the folder.
But because icons can be used multiple times on the same card, you need an easy way to assign
them later in the card settings. And that's the job of the **standard.toml** found in this
folder::

    [icons]
    attack = "attack.png"
    defense = "defense.png"
    fire = "element_fire.png"

This file assigns every icon file to a unique 'name' to be used for referencing it in the card
settings later on. This is one of the rare cases where the key name you assign the icon file to
is completely up to you.

3.3 Fonts
---------
Believe it or not, but without any text on your playing cards you'd be pretty limited in your
game design options (except you're just building a game like memory - but you wouldn't need
CARDmage for that).

This folder contains all your font files (doesn't really matter if you separate each font
family in their own subfolder or not as long as you adjust the configuration accordingly) and
to give you a little kickstart the base package found in the 'release' section on GitHub
contains already six open source fonts (SIL licensed) – three serif, three sans-serif – ready
to be used in your project.

To make those font files usable for CARDmage we need a bit of configuration this time - but
that's usually a one-time task. For that you need to create what I'd call a 'font set'. It
tells CARDmage which font to use in which font size and for which part of the card.

Have a look at the **standard.toml** file found in *testdata/fonts*. It contains a lot of
blocks and many definitions. But let's break it down a little bit. All you need to make it
work are the **[config]** and **[default]** blocks. So let's focus on them first::

    [config]
    font_normal = "Sansation/Sansation.ttf"
    font_bold = "Sansation/SansationB.ttf"
    font_italic = "Sansation/SansationI.ttf"
    font_light = "Sansation/SansationL.ttf"

    [default]
    fontcolor = "black"
    fontsize = 24
    fontstyle = "normal"
    textalign = "left"
    # textdecoration = "underline"

The config-block points to the actual font files to be used by CARDmage – once again relative
to the directory this file is contained in. It contains one definition for each font-style
used later on (like **bold** or *italic*). But with that information alone CARDmage doesn't
know how the text on the card should be rendered. That's specified within the default-block.

The default-block contains the fallback rules used for all text displayed on a card, **unless**
specified otherwise for individual text blocks. Definitions deactivated with a hashtag in the
example above are optional (built-in defaults will be used if they're not specified),
all other definitions are mandatory.

Overriding Defaults
'''''''''''''''''''
So what if a certain text block on the card is supposed to have another text color? That's
where the concept of **modular layouts** comes into play. We'll go into the details what modular
layouts are and how they work in the next chapter. But in a nutshell, you can define different
values for individual text areas by doing so within a **modules** block. This is how it would
look like::

    [modules.type]
    fontsize = 30
    fontstyle = "bold"

This instructs CARDmage to use for text displayed inside the 'type' module the default values
for fontcolor (*black*) and textalign (*left*) as well as the module-specific values for
fontsize (*30*) and fontstyle (*bold*).

3.4 Templates & Layouts
-----------------------

Templates
'''''''''
Now we come to the more interesting parts of configuring your own playing cards. A template in
this context describes an image file used as an overlay that adds the overall structure to a
card. It contains all of the graphical structures and design elements common to a larger
number of cards. As an example: Imagine a standard Pokémon card and take away all texts, the
different element icons (since Pokèmon can have different types, we'd need a lot of different
templates to cover all possible combination of icons possible, so let's remove them from the
basic card structure) and the card's artwork – and what's left would be in our case the card's
**template**.

Now that we have our artwork and a template, our progress is already visible. We can even
see where the texts and the card's title are supposed to be. Just one problem: CARDmage
doesn't know it (yet).

Layouts
'''''''
That's where the template's configuration file (also referred to as **layouts**) comes into
play. Each layout belongs to exactly one template. If you open one of the TOML files
inside the *testdata/layouts*, you'll find something like this::

    [config]
    image_zone = [0, 0]
    image_credits_zone = []
    title_zone = [60, 89]
    title_zone_dimensions = [560, 40]

    [icons]
    set = "standard"

    [image]
    use_vertical = true

    [modules]
    attributes_zone = [
        [672, 117],
        [672, 177],
        [672, 237]
    ]
    attributes_zone_dimensions = [35, 40]
    attributes_zone_icon_offset = [-42, -5]
    edition_icon_zone = [627, 576]
    edition_icon_zone_dimensions = [90, 100]
    legendary_zone = [52, 260]
    legendary_zone_dimensions = [25, 316]
    meta_id_zone = [309, 984]
    meta_id_zone_dimensions = [120, 36]
    resources_zone = [60, 927]
    resources_zone_dimensions = [620, 48]
    text_zone = [60, 656]
    text_zone_dimensions = [620, 264]
    type_zone = [60, 607]
    type_zone_dimensions = [340, 56]

    [template]
    background = "black"
    file = "bezirk.png"
    size = [738, 1033]

As you see a layout contains the coordinates needed to put all the elements of the card into
place. But let's tear it down from top to bottom.

**config**: The config block contains the coordinates needed for the mandatory content of a
card – it's title and it's artwork. It also specifies the maximum size of the card's title
(needed to avoid a possible out-of-bounds rendering of long texts).

**icons**: This block contains a single key called 'set'. It is used to tell CARDmage which
icon set it should use for cards using this layout. Enter here the file name of the desired
icon configuration without the ".toml" ending (in this example "standard" refers to the file
used as an example in chapter 3.2).

**image**: Specifies if the current layout supports vertical oriented artworks.

**modules**: Here you'll define every content area you need on your card (except the two most
important ones from the [config] block). You can define as many content areas ("modules") as
you like or need, but be sure to give each module a unique name::

    #  <name>_zone
    legendary_zone = [52, 260]
    #  <name>_zone_dimensions
    legendary_zone_dimensions = [25, 316]

Each module consists of two keys here: *<name>_zone* (the coordinates of the modules' top left
corner) and *<name>_zone_dimensions* (the size of the module). The unique name allows CARDmage
to assign the card's contents to their correct destination areas.

But how do you assign content or custom styling to a module? Let's have a look at the second
example in chapter 3.3::

    # modules.<name>
    [modules.type]
    fontsize = 30
    fontstyle = "bold"

This part of the font definition only applies to the module named 'type'. All other modules
will ignore these settings. You'll later assign content to a module in very much the same way:
Create a *[modules.<name>]* block and it's contents will be rendered in the card's area
defined by *<name>_zone* and *<name>_zone_dimensions*. This gives you precise control about
what goes where on your cards.

**template**: This block connects the layout with it's template counterpart ('file'), defines
the card's background color ('background') and specifies the overall size of the card ('size'
– in pixels).