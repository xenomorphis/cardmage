CARDmage Changelog
==================

Version 1.3.0
'''''''''''''
*Aug 08, 2023*

* **[REMOVAL]** Removes card definition entries ``source_hd`` and ``source_vertical_hd``
* **[REMOVAL]** Removes layout definition entry ``image_credits_zone`` (wasn't in use anyway)
* Adds a command line option for specifying the desired output image format
* Adds support for the `QOI image format <https://qoiformat.org/>`_
* Code quality: Handles some possibly thrown exceptions related to the the ``array`` content element
* Code cleanup: Replaces concatenated strings in print statements with f-strings

Version 1.2.0
'''''''''''''
*Feb 19, 2023*

* **[BREAKING]** Removes support for multiple ``paragraph`` content elements inside the same module (was introduced in version 1.0.1)
* **[BREAKING]** Removes support for ``paragraph`` aliases (was introduced in version 1.0.1)
* Adds support for named content elements, a simpler but more powerful variant of the above features
* Fixes CARDmage skipping whole cards in translation mode if the corresponding translation file is corrupted or missing
* Simplifies some code fragments
* Documentation: Adds detailed explanations for each available content element

Version 1.1.1
'''''''''''''
*Dec 17, 2022*

* Adds an option to change the list bullet from dash to dot
* Fixes missing fallback value for 'fontcolor' in case no default font color was given by the user
* Various documentation updates

Version 1.1.0
'''''''''''''
*Nov 28, 2022*

* Implements support for card translations
* Adds documentation for feature set v1.1.0

Version 1.0.1
'''''''''''''
*Oct 11, 2022*

* Implements support for multiple paragraph elements in the same rendering zone
* Implement all variables loaded from TOML files as global variables
* Fixes dynamic font size adjustments made when a text is too large for it's rendering zone
* Reworks the internal assignment of font settings
* Removes an obsolete function
* Some code cleanup here and there

Version 1.0.0
'''''''''''''
*Sep 27, 2022*

* Includes optimizations for content elements rendered directly after a 'prefix' element
* Adds the new attribute ``code`` to the card TOML files (used as the output's filename)
* Disables saving of build artefacts in exchange for a considerable performance boost
