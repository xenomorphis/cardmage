4. How to build your own card game - Card contents
==================================================
Now we set the stage to add the actual content to all the preparations we've done so far.
And all you need to do is adding a TOML file to the *cards* folder and filling it with the
content you want. Let's have a look at an example::

    [card]
    back = ""
    element = "neutral"
    font = "standard"

    [image]
    source = "AetherSchmiede.png"
    source_hd = "AetherSchmiede.png"
    source_vertical = "AetherSchmiede.png"
    source_vertical_hd = "AetherSchmiede.png"
    artist = "xenomorphis"

    [layout]
    type = "bezirk"
    # background = "white"

    [meta]
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
