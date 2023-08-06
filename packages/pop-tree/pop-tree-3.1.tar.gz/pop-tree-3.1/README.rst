********
POP-TREE
********
**POP hub and sub visualization tool**

INSTALLATION
============
::
    pip install pop-tree

INSTALLATION FOR DEVELOPMENT
============================

Clone the `pop-tree` repo and install with pip::

    git clone https://gitlab.com/Akm0d/pop-tree.git
    pip install -e pop-tree

EXECUTION
=========

After installation the `pop-tree` command should now be available.

Example using a vertically merged project:
.. code-block:: bash

    pop-tree exec --add-sub idem


Example of printing hub.OPT for config defaults:
.. code-block:: bash

    pop-tree opt --add-sub tiamat
