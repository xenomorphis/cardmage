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
The following blocks and /or keys are always needed and will likely cause CARDmage to fail if
not present:

**title**

| This key contains the name of the card. For obvious reasons this key should never be omitted
  or left empty.

**card**

| The 'card' block defines the image file used for the card's back (*'back'*) and the
  font set used for text rendering (*'font'*).
| Important to know: You don't need to add the file extension if you're referencing a TOML
  file. For image files however you need to add the file extension, because of the different
  formats a image file can have (PNGs, JPEGs, ...). Folder names or complete paths can be
  omitted if the file you're referencing to can be found in it's pre-defined folder (the one
  you set in the settings.toml in chapter 2).

**image**

| This block contains the file names of the card's artwork. You can use different images
  depending on the layout's support for vertical artworks. CARDmage will use the
  standard image for the normal processing mode and the HD image for print quality mode (see
  `chapter 5 <https://github.com/xenomorphis/cardmage/blob/main/docs/Usage.rst>`_ for more
  information about the different processing modes available within CARDmage).

**layout**

| You need to assign a layout to each card by adding the name of the layout's TOML
  definition file to the *type* key. In this example the card uses the layout specified in
  the *bezirk.toml* found inside the *layouts* folder.