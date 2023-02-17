ADDENDUM B: Configuration reference
===================================

This addendum contains information about all configuration options supported and used by CARDmage.

B.1 Font settings
-----------------
The following settings can be used to change the appearance of card texts in various aspects.
They'll work almost anywhere inside font definitions and inside card modules (see
`chapter 3.3 et seq. <https://github.com/xenomorphis/cardmage/blob/main/docs/CardSetup.rst>`_)
unless specified otherwise.

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - bullet
      - Defines the style of all bullets in a list. CARDmage currently supports either dots or dashes.
      - ``dash``, ``dot``
      - ``bullet = "dash"``
      - yes² (default value: ``dash``)
    * - font
      - Defines the font to be used for a specific **font style** (see below). This parameter must be used with a suffix declaring the font style this entry is related to (for example ``font_normal`` defines the font file to be used for *normal* styled text). You must declare at least one font style inside the ``[config]`` section of each font set.
      - a valid filename
      - ``font_normal = "Sansation/Sansation.ttf"`` or ``font_bold = "Sansation/SansationB.ttf"``
      - no
    * - fontcolor
      - Defines the text color. This settings accepts a list of predefined named colors as well as RGB(A)/HSL(A)/HSB(A)/CMYK(A) colors in decimal or hexadecimal notation. You can find a more in-depth explanation `here <https://www.imagemagick.org/script/color.php>`_.
      - ``white``, ``aqua``, ``#8DEEEE``, ``rgba(255, 0, 0, 1.0)``
      - ``fontcolor = "white"``
      - yes (default value: ``black``)
    * - fontsize
      - Defines the text size in pixels
      - any positive number
      - ``fontsize = 38``
      - no¹
    * - fontstyle
      - This setting defines which font style should be used for text rendering, for example "normal" or "bold". Make sure you have defined a **font** file for the font style you want to use.
      - any string, but either ``normal``, ``bold``, ``italic`` or ``bolditalic`` are recommended
      - ``fontstyle = "bold"``
      - no¹
    * - outline
      - This setting consists of two named parameters ('color' and 'width') and defines the text outline's color and its width.
      - **color:** a valid color (see *fontcolor* for further information); **width:** any positive number
      - ``outline = {color = "black", width = 1.5}``
      - yes (default value: ``{color = "none", width = 1}``)
    * - textalign
      - Defines the alignment of a text or image.
      - either ``left``, ``center`` or ``right``
      - ``textalign = "left"``
      - yes (default value: ``left``)
    * - textdecoration
      - Defines if any decorations should be applied to the text.
      - either ``no``, ``underline``, ``overline`` or ``line_through``
      - ``textdecoration = "underline"``
      - yes (default value: ``no``)

Annotations
'''''''''''
| ¹: This setting has to be defined at least once inside the ``[default]`` section of each font set.
| ²: This setting has no effect if not used in ``[tags.list]`` or inside a module containing a ``list`` content element.


B.2 Content elements
--------------------
| Content elements are used to add different types of content like texts or images to a card. This chapter provides
  detailed descriptions, usage guides and lists containing the mandatory and optional settings for each content element.
| All configurations and features described in this section are only relevant inside card definition files (and card
  translation files since their contents are derived from the card definitions) as mentioned in
  `chapter 4.2 <https://github.com/xenomorphis/cardmage/blob/main/docs/CardContents.rst>`_.

image
'''''
The **image** content element renders an image inside the current module.

| The alignment of the image inside the module is determined by the ``textalign`` setting. Other font settings are
  irrelevant for this content element.
| Important note: The image CE does **not** advance or update the rendering offset. Any text-based content element
  following right after an image element will cause the text to be rendered on top of the image.
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - image
      - Filename of the image you'd like to render
      - any valid filename
      - ``image = "background2.jpg"``
      - no

prefix
''''''
The **prefix** content element renders a short text inside the current module and doesn't include a line feed at it's
end.

| All font settings except ``bullet`` apply for this content element.
| Prefixes were designed to add short texts with a different formatting in front of paragraph elements. They share a lot
  of similarities with the **condition** elements described below, the only notable difference being the missing line
  feed after a prefix element. Each content element succeeding a **prefix** element starts in the same line the prefix
  ended in.
| Texts rendered as a prefix shouldn't exceed one line in length.
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - prefix
      - Contains the text fragment to be rendered
      - any text string
      - ``prefix = "Resources:"``
      - no

condition
'''''''''
The **condition** content element renders a short text inside the current module and includes a line feed at it's end.

| All font settings except ``bullet`` apply for this content element.
| Conditions were designed to add short texts with a different formatting in front of paragraph elements. The main
  difference between a condition and a prefix is the line feed inserted after conditions. Each content element
  succeeding a **condition** element starts in a new line.
| Texts rendered as a condition shouldn't exceed one line in length (longer conditions don't pose a problem in most cases
  though).
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - condition
      - Contains the text fragment to be rendered
      - any text string
      - ``condition = "At the end of your turn:"``
      - no

paragraph
'''''''''
The **paragraph** content element is the main element for adding any amount of text to a card. A small amount of
whitespace and a line feed will be added after a paragraph.

| All font settings except ``bullet`` apply for this content element.
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - paragraph
      - Contains the text to be rendered
      - any text string
      - ``paragraph = "Enter as much text here as you like"``
      - no

list
''''
The **list** content element is quite obviously used for rendering unordered lists. Adding support for ordered lists is
planned for a future release.

| All font settings apply for this content element.
| The ``bullet`` font setting determines, if either dashes or dots are used as bullets.
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - list
      - Contains the list items to be rendered
      - a list containing one or more text strings
      - ``list = ["List point 1", "List point 2", "List point 3"]``
      - no

icons
'''''
The **icons** content element is used to render one or more icons inside a module. It is one of the two content elements,
which supports modules with multiple rendering zones (the other one being the array element).

| Font settings don't affect this content element.
| In contrast to the image element the **icons** element allows more than one image file to be rendered. If the module
  consists of more than one rendering zone, the CE will render one icon into each zone: The first given
  icon inside the first given rendering zone, the second item inside the second given rendering zone and so on. This
  loop stops when CARDmage runs out of rendering zones to fill or icons to render. In a best-case scenario you'd have
  the same amount of icons and rendering zones.
|
| Available settings:

.. list-table::
    :widths: 100 140 100 100 70
    :header-rows: 1

    * - setting
      - usage / description
      - possible values
      - example
      - optional
    * - icons
      - Contains a list of icon names
      - a list containing one or more text strings
      - ``icons = ["fire_mana", "ice_mana", "lightning_mana"]``
      - no
