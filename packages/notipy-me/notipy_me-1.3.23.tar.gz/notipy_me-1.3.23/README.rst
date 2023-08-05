Notipy Me
=============
|sonar_quality| |sonar_maintainability| |sonar_coverage| |pip| |downloads|

A simple python package to send you and any other receiver an email when a portion of code is done running.

A special callback for Keras is now available to get automatic reports for the training of a model.

Setup
-----

Just run:

.. code:: bash

   pip install notipy_me

The keras callback will be automatically available if tensorflow is installed.

Preview
--------------------------
There are 4 emails types: 

- start: notify the recipients that the task has started.
- report: send out the logged reports after a given interval.
- exception: notify the recipients that the task has been interrupted.
- completed: notify the recipients that the task has completed.

|preview|

Usage example
-------------
A basic usage example can be the following:

Usage as decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from notipy_me import Notipy

    @Notipy
    def my_long_running_script():
        ...

Usage as context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from notipy_me import Notipy
    from time import sleep
    import pandas as pd

    with Notipy() as ntp:
        for i in range(1000):
            ntp.add_report(pd.DataFrame({
                "test":[2]
            }))
            sleep(1)

Usage in a Keras model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from notipy_me import KerasNotipy

    my_keras_model = build_my_keras_model(...)
    my_keras_model.fit(
        X, y,
        callbacks=[
            KerasNotipy(
                task_name="Training BERT"
            )
        ]
    )


Form example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you run the script Notipy will ask you to enter your email, password etc... it will store into a cache file called `.notipy` every setting except for the password.

|usage|

Known issues
------------

Gmail
~~~~~
I cannot manage to get Gmail to work, but it keeps rising an error
logging in with the credentials, even though they are correct. With the
other mail providers it works fine.

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_notipy_me&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_notipy_me

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_notipy_me&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_notipy_me

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_notipy_me&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_notipy_me

.. |pip| image:: https://badge.fury.io/py/notipy-me.svg
    :target: https://badge.fury.io/py/notipy_me

.. |downloads| image:: https://pepy.tech/badge/notipy-me
    :target: https://pepy.tech/badge/notipy-me
    :alt: Pypi total project downloads 


.. |preview| image:: https://github.com/LucaCappelletti94/notipy_me/blob/master/preview.png?raw=true
.. |usage| image:: https://github.com/LucaCappelletti94/notipy_me/blob/master/notipy.gif?raw=true