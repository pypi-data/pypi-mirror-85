.. _sec_installation:

============
Installation
============

Requirements
------------

``Demes`` uses `srictyaml <https://github.com/crdoconnor/strictyaml>`_ to 
read YAML-defined demographic models.

Installation
------------

Currently, ``demes`` is most useful for simulation software developers who
want to support demographic models imported from ``demes`` descriptions.

Installation instructions for developers:

.. code-block::

   ## Clone the repository
   $ git clone https://github.com/grahamgower/demes.git
   $ cd demes
   
   ## Install the developer dependencies
   $ python -m pip install -r requirements.txt
   
   ## Run the test suite
   $ python -m pytest -v tests


