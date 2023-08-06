ConcurrentEvents
================
.. image:: https://gitlab.com/Reggles44/concurrentevents/badges/master/pipeline.svg
    :alt: pipeline status
    :target: https://gitlab.com/Reggles44/concurrentevents/-/commits/master

.. image:: https://gitlab.com/Reggles44/concurrentevents/badges/master/coverage.svg
    :alt: coverage report
    :target: https://gitlab.com/Reggles44/concurrentevents/-/commits/master

.. image:: https://readthedocs.org/projects/concurrentevents/badge/?version=latest
    :target: https://concurrentevents.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

``ConcurrentEvents`` is a light weight event system and threading tools build around the concurrent futures library.

The aim of this project is to create an extremely simple and generic event system as well as tools to monitor and use it effectively.

The focus of this project is based around the ``ConcurrentEvents.EventManager``, ``ConcurrentEvents.EventHandler``, ``ConcurrentEvents.Event`` classes and ``ConcurrentEvents.Catch`` decorator to create a simple and safe way to do multi-threading through an event framework.

Installation
------------
``ConcurrentEvents`` should be installed through pip on ``python3.5`` or higher

.. code-block:: bash

    python -m pip install ConcurrentEvents
    
Usage
-----

ConcurrentEvents is used similar to other event systems where by decorators are used to map functions to events.
This simple example shows a hello world run through the event system but catching the `Start` event

.. code-block:: python

    from ConcurrentEvents import EventManager, catch, Start

    @catch(Start)
    def hello_world():
        print("Hello World")

    EventManager().start()

A more complicated example might involve having one event trigger more.
In the following example a custom `Event` is created to handle outputting counting.
Additionally the `CountingEventHandler` class is made as a subclass of `EventHandler` so that it can use the build in functionality of firing and canceling events.

.. code-block:: python

    from ConcurrentEvents import EventManager, EventHandler, catch, Start, Event

    class CountEvent(Event):
        pass

    class CountingEventHandler(EventHandler):
        @catch(Start)
        def start_counting(self):
            for i in range(10):
                self.fire(CountEvent(i))

        @catch(CountEvent)
        def print_count(self, i):
            print(i)

    EventManager().start()

Using the same example of counting there is also functionality to cancel an event or simply trigger exit.
The following code will cancel when `i` is equal to 5.
At the same time, if `i` is equal to 8 the exit event will fire which stops all functionality and goes to cleanup.

.. code-block:: python

    from ConcurrentEvents import EventManager, EventHandler, catch, Start, Event, Exit

    class CountEvent(Event):
        pass

    class CountingEventHandler(EventHandler):
        @catch(Start)
        def start_counting(self):
            for i in range(10):
                self.fire(CountEvent(i))
                if i == 5:
                    self.cancel()
                if i == 8:
                    self.fire(Exit())

        @catch(CountEvent)
        def print_count(self, i):
            print(i)

    EventManager().start()
