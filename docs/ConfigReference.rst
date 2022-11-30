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
      - Defines the style of all bullets in a list. CARDmage currently supports either dots or dashes. **NOTE:** This setting has no effect when used outside of ``[tags.list]``
      - ``dash``, ``dot``
      - ``bullet = ["dash"]``
      - yes