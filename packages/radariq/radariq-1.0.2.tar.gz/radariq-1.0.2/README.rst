=================================
Python SDK  |docs|
=================================


Overview
========
This module provides an easy to use Python wrapper for the RadarIQ-M1_ sensor which works
for both Python 2 & 3. This SDK has been tested with Windows, OSX, Raspberry Pi and Linux.

The RadarIQ-M1 sensor is an easy-to-use radar sensor for detecting objects and measuring distance and speed.
All the difficult parts of working with radar are done by the sensor and a simple API and SDK provide an easy
path to integration.

- Project Homepage: https://github.com/radariq/python-sdk
- Download Page: https://pypi.python.org/pypi/radariq

The RadarIQ Python SDK is released under the MIT software license, see LICENSE_ for more details.

.. _LICENSE: https://github.com/radariq/python-sdk/LICENCE


Documentation
=============
See https://radariq-python.readthedocs.io


Requirements
============
- Python_ 2 or 3
- A RadarIQ-M1_ module

Installation
============

Install the RadarIQ SDK using pip

.. code-block:: bash

    pip install radariq

The SDK can be used from Python scripts

.. code-block:: python

    from radariq import RadarIQ

Usage
======

.. code-block:: python

    from radariq import RadarIQ, MODE_POINT_CLOUD

    riq = RadarIQ()
    riq.set_mode(MODE_POINT_CLOUD)
    riq.set_units('m', 'm/s')
    riq.set_frame_rate(5)
    riq.set_distance_filter(0, 10)
    riq.set_angle_filter(-45, 45)
    riq.start()

    for row in riq.get_data():
        print(row)


Examples
========
Examples are in the directory examples_.


Other pages
===========

- `Home page`_
- `Downloads`_
- `GitHub`_
- `Forum`_
- `Youtube channel`_
- `Facebook page`_

.. _`GitHub`: https://github.com/radariq
.. _`Home Page`: https://radariq.io
.. _`Downloads`: https://radariq.io
.. _`Forum`: https://forum.radariq.io
.. _`Youtube channel`: https://youtube.com/radariq
.. _`Facebook page`: https://facebook.com/radarIQsensing
.. _`Python`: https://www.python.org
.. _`RadarIQ-M1`: https://radariq.io/products/radariq-m1
.. _`radariq.io`: https://radariq.io
.. _examples: https://github.com/radariq/python-sdk/blob/master/examples

.. |docs| image:: https://readthedocs.org/projects/pip/badge/?version=stable
   :target: https://pip.pypa.io/en/stable/?badge=stable
   :alt: Documentation Status