Planned Features
================
Since this project is still in an early stage of development, the primary goal is completing the most basic features for now. But the following features are already likely to get implemented in the future (but not necessarily in this particular order):

1. Modular layouts
------------------
Render small sections of a layout only if needed in pre-defined areas - f. e. rendering a card attribute only if it's value is greater than 0. This can significantly reduce the amount of prepared layouts needed to cover every possible card content.

This feature requires a lot of planning and testing to keep it as intuitive as possible to use. Therefore it will most likely be shipped as it's own major update.

2. Card rarities and meta content rendering
-------------------------------------------
Card rarities are not yet represented in a cards TOML file. This will be fixed soon.

The bigger part of this feature covers the meta content like card rarities, copyright information and card number as well as their representation (and possible ways of changing / defining it) on the final card.

3. Card translations
--------------------
Implement an easy way to add translation overrides to any given card content and build translated cards automatically via command line switch.

4. Auto-Mode
------------
Implement an option (via command line switch) to build all available cards automatically (batch-mode).