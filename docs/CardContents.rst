4. How to build your own card game - Card contents
==================================================
Now we set the stage to add the actual content to all the preparations we've done so far.
And all you need to do is adding a TOML file to the *cards* folder and filling it with the
content you want. Let's have a look at an example::

    title = "Die Aetheriumschmiede"

    [card]
    back = ""  # currently not in use
    font = "standard"

    [image]
    source = "AetherSchmiede.png"
    source_hd = "AetherSchmiede.png"
    source_vertical = "AetherSchmiede.png"
    source_vertical_hd = "AetherSchmiede.png"

    [layout]
    type = "bezirk"
    # background = "white"

    [meta]
    artist = "xenomorphis"
    edition = "PRE"
    id = "000"
    language = "DE"
    version = "2201"
    year = "2022"

    [modules.attributes]
    array = [0, 6, 3]
    keys = ["attack","defense","hp"]
    keys_as = "icons"

    [modules.meta_id]
    paragraph = "{edition}-{id}"

    [modules.resources]
    array = [0, 1, 0, 0, 0, 0, 0]
    keys = ["Gold", "Feuer", "Wasser", "Wind", "Licht", "Schatten", "Ehre"]
    keys_as = "text"
    prefix = "Ressourcen: "

    [modules.text]
    content = ['condition', 'list']
    condition = "Solange auf dem Feld:"
    list = [
        "Der Spieler kann Dwemer-Kreaturen in die Schlacht rufen.",
        "Rekrutierungskosten von Dwemer-Kreaturen sind um 1 Gold reduziert."
    ]

    [modules.type]
    paragraph = "Bezirk - Dwemer"

As you see there's a lot of stuff going on in a card's configuration file. For the sake of
simplicity I'll only go through the file's overall structure and the different content elements
here. For an in-depth explanation of the different attributes please refer to the
`Configuration reference <https://github.com/xenomorphis/cardmage/blob/main/docs/ConfigReference.rst>`_.

4.1 Must-have configurations
----------------------------
The following blocks and/or keys are always needed and will likely cause CARDmage to fail if
not present:

title
'''''
| This key contains the name of the card. For obvious reasons this key should never be omitted
  or left empty.

card
''''
| The 'card' block defines the image file used for the card's back (*'back'*) and the
  font set used for text rendering (*'font'*).
| Important to know: You don't need to add the file extension if you're referencing a TOML
  file. For image files however you need to add the file extension, because of the different
  formats a image file can have (PNGs, JPEGs, ...). Folder names or complete paths can be
  omitted if the file you're referencing to can be found in it's pre-defined folder (the one
  you set in the settings.toml in chapter 2).

image
'''''
| This block contains the file names of the card's artwork. You can use different images
  depending on the layout's support for vertical artworks. CARDmage will use the
  standard image for the normal processing mode and the HD image for print quality mode (see
  `chapter 5 <https://github.com/xenomorphis/cardmage/blob/main/docs/Usage.rst>`_ for more
  information about the different processing modes available within CARDmage).

layout
''''''
| You need to assign a layout to each card by adding the name of the layout's TOML
  definition file to the *type* key. In this example the card uses the layout specified in
  the *bezirk.toml* found inside the *layouts* folder.

4.2 Optional configurations
---------------------------
The following settings and sections represent the card's contents and are purely optional.
Use them as you need 'em.

meta
''''
| The meta block contains any number of single line text snippets. You can name the keys
  however you want and those keys defined here will not be rendered initially, but you can
  insert those text snippets in any module via **meta tags**.
| As an example: If you defined a meta key like this ``copy = "©2022 ACME Inc."`` you can
  easily insert this copyright information into any module by adding the corresponding meta
  tag ``{copy}`` into one of it's content elements.

modules
'''''''
| The modules block contains the actual content to be displayed on the card. The name of the
  module is used to determine where on the card the content of a module will be rendered (see
  chapter 3.4 for an example).
| CARDmage supports some predefined keys for displaying content (called **content elements (CEs)**.
  Depending on how you want your content to be rendered you'll have to use the corresponding
  content element. In this chapter I'll give you a brief overview over the CEs offered by
  CARDmage and when to use them.

.. list-table::
    :widths: 70 70 140 70 70
    :header-rows: 1

    * - key
      - render priority
      - used for
      - allows other content elements in the same module
      - forces new line for next content element
    * - ``image``
      - 0
      - renders a given image inside the module
      - yes
      - yes
    * - ``prefix``
      - 1
      - displaying a different formatted text at the beginning of a module **without** introducing a line-feed at it's end
      - yes
      - no
    * - ``condition``
      - 10
      - displaying a different formatted text or headline at the beginning of a module **with** a line-feed at it's end
      - yes
      - yes
    * - ``paragraph``
      - 20
      - displays a simple text element. Line breaks will be added automatically by CARDmage if needed
      - yes
      - yes
    * - ``list``
      - 30
      - renders a set of texts as an bulleted list
      - yes
      - yes
    * - ``icons``
      - 40
      - fills multiple zones with different icons
      - no
      - no
    * - ``array``
      - 50
      - special content element used for filling multiple zones dynamically with similar content or creating a dynamic list in a single zone
      - yes, when used in a single zone only
      - there's no 'next content element'

| If there's more than one content element present in a module the order in which the
  individual content elements are rendered onto the card depends on the priority values as seen
  in the table above. Content elements with a lower priority value will be rendered before those
  with a higher priority value.
| You can however define your own priority list within the optional ``content`` attribute
  (that's useful if you want to render for example a *condition* first, then a *list* and
  finally adding a *paragraph* below that).

You can find more details about how the different content elements work in the
`configuration reference (Chapter 7) <https://github.com/xenomorphis/cardmage/blob/main/docs/ConfigReference.rst>`_
