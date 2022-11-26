5. How to build your own card game - Translating cards
======================================================
Starting with version 1.1.0 CARDmage is able to generate the same card in multiple languages.
This is made possible via a separate TOML file containing the translated text fragments and
a new setting in the card's configuration file.

Let's have a closer look on how this works.

5.1 The translation file
------------------------
You might have already spotted the *translations* folder inside the project directory. It was
unused in previous CARDmage versions, but that changes RIGHT NOW! Inside the folder you'll
find two TOML files – one for each card configuration file inside the *cards* folder and with
exact the same filename. That's important, because CARDmage will connect a card with it's
translations 'counterpart' via the matching filename.

Both translation files are similar in their structure, so it's quite irrelevant which one you
want to examine. But I'll go with :code:`B_Aetheriumschmiede.toml` here::

    [original]
    # This section contains all texts of a card that need to be translated.
    # It is optional, since this section will not be used by CardMage, but it may be used by the translators as a template.
    title = "Die Aetheriumschmiede"

    [original.meta]
    language = "DE"

    [original.modules.resources]
    prefix = "Ressourcen: "

    [original.modules.text]
    condition = "Solange auf dem Feld:"
    list = [
        "Der Spieler kann Dwemer-Kreaturen in die Schlacht rufen.",
        "Rekrutierungskosten von Dwemer-Kreaturen sind um 1 Gold reduziert."
    ]

    [original.modules.type]
    paragraph = "Bezirk - Dwemer"


    ### Start Translation EN
    [translations.en]
    title = "The Aetherium Forge"

    [translations.en.meta]
    language = "EN"

    [translations.en.modules.resources]
    prefix = "Resources: "

    [translations.en.modules.text]
    condition = "While on the field:"
    list = [
	    "The player may summon Dwemer-type creatures.",
	    "Recruitment costs of Dwemer creatures are reduced by 1 gold."
    ]

    [translations.en.modules.type]
    paragraph = "District - Dwemer"

As you might have already spotted: This file isn't just a copy of the card definition but with
english texts instead of german ones. I could have done that, but there are three reasons, why I
did things differently:

* **Consistency**: Imagine you have to buff or nerf a card in the future. You're changing the original
  card effect accordingly, but since you don't speak all of the six available languages for that
  card you're deciding to save your changes and update the translations at a point somewhere in
  the future. If the translations are in the same file as the original card text they're based on
  it is not easy to tell for others from looking at the file alone if the changes to the cards
  effect have already been reflected in the translations. The card definition file has a new
  timestamp (because you've saved your changes), but were the translations updated too?.
  If you have the translations and the card text in two separate files you can already tell from
  comparing the files timestamps if the translations are up-to-date or for example two months
  behind the card's definition file.
* **Simplicity**: One might argue why for simplicity's sake it should be easier to edit content
  in two files instead of one. I have to admit it might be a matter of taste, but if you write
  everything in one file it gets more and more complex and confusing the more content you're
  putting in – especially for people new to the project. From a developers perspective it is a
  lot easier to introduce new major features as a new module instead of including them in an
  already working module (and overloading or crashing it in the process) – it leans the whole
  process of coding, testing and debugging software.
* **Responsibility**: If you have a larger team working on a card game, you might want to share
  responsibilities between your teammates. If the people responsible for game design aren't the
  translators at the same time it has always been a good idea to give everyone exact as much
  information as they need to complete their task. Not because you can't trust them, but because
  you don't need to in this case. If you give them a complete card definiton file they might
  want to add their own 'flavour' to the card's functionality – and that's rarely a step forward,
  but mostly a step to the side.
