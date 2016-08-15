
.. _authorguide:

Author Guide
============


**Symbolic variables**

.. https://groups.google.com/forum/?fromgroups#!searchin/sage-support/SR$20VAR/sage-support/PhOoNyALRX0/pYRFT_duKQoJ

Inside an exercise class one should use

.. code-block:: python

   x1 = SR.var('x1')

to create variables for expressions like:

.. code-block:: python

   expr = x1^2+3

that can be used in calculations, integrated for example:

.. code-block:: python

   integrate(x1^2+3,x1)

.. python






