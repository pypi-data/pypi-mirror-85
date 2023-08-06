Flask
=====

pylivereloader is a lightweight script reloader.
It's designed to maintain a running script at it's live version.
For example if you're coding the script to maintain live with LiveReloader the script you're coding will always run at it's latest version based on his last modification time.

Installing
----------

Install and update using `pip`_ :

.. code-block:: text

    pip install -U pylivereloader


A Simple Example
----------------

.. code-block:: python

    from pylivereloader import LiveReloader

    maintainer = LiveReloader("myscript",
                                safe_reload = True,
                                logging = True)

    def do () :
      myscript.function()

    maintainer.keep_live(do)

Links
-----

* Website: https://github.com/Z3R0xLEGEND
* Official chat: https://discord.gg/VeeZnVY
* Releases: https://pypi.org/project/pylivereloader/

.. _pip: https://pip.pypa.io/en/stable/quickstart/
