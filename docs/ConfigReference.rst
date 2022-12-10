ADDENDUM B: Configuration reference
===================================

Introductory remarks
''''''''''''''''''''
The following tables contains all configuration options supported by CARDmage and may serve as the
official configuration reference.

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
      - ``bullet = ["dash"]``
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
      - Defines the alignment of a text.
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