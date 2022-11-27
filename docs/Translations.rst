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

A translation file contains only two sections and one of them is completely optional.

Section 'original'
''''''''''''''''''
The first one is the *'original'* section. You should (but not must) copy all original texts that need
to be translated into this section **while keeping the hierarchy intact**, so your translators are
able to use it as a template or starting point for their translations. If you have a look at the
example above you'll find all german texts from the card definition file in the corresponding spot
inside the *original* section (the *title* can be found in *original.title*, the module
*modules.text* can be found in *original.modules.text* etc.).
Note: CARDmage will ignore this section completely, so you won't run in any errors even if you've messed
up the file hierarchy inside this section. But it might introduce some errors later on, if the
translators are using it as a template for the translations.

Section 'translations'
''''''''''''''''''''''
The second section called *'translations'* is the more important one. It contains a subsection
for each language a card is translated into:

* :code:`translations.en.*` for the english translation,
* :code:`translations.de.*` for the german translation,
* :code:`translations.it.*` for the italian translation, etc.

Because there are some international standards regarding language codes, it is recommended to use
the abbreviations defined in `ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_
here.

The translated texts inside the subsections need to reflect the hierarchy from the card definition
file. Let's review the two examples from earlier: *title* must be placed in *original.title* for
the *'original'* section and in *translations.<language_code>.title* for the *'translations'*
section. Following the same pattern *modules.text* must be placed in *original.modules.text*
(for the template) and in *translations.<language_code>.modules.text* (for the actual translations).

Workflow
''''''''
So you might ask "What is now the purpose of having the *'original'* section at all?".
The basic workflow is as follows: If there's a *'original'* section all the translator has to do is
copying the entire section, pasting it at the end of the file and replacing the *'original'* in
the name of the newly added sections with *'translations.<language_code>'*. Of course the
translator should then translate the card texts after that, but at this point the newly created
translations subsection is ready to be used by CARDmage.

Design considerations
'''''''''''''''''''''
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
