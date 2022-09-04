3. How to build your own card game
==================================
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

3.2 Fonts
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

**Overriding Defaults**

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
