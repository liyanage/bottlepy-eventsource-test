
# Python web framework tests for Server-Sent Events

I have some python tools with a localhost-only, [bottle.py][bottle] web based user interface.
I want the server (Python) to send events to the client (JavaScript) via [Server-Sent Events][sse] (EventSource API).

That doesn't work with Bottle's default `wsgiref` server because it is single-threaded
and SSE leaves the connection open, so I need a solution that is able to serve at least
two connections at the same time.

I tested some of the multithreaded extension options supported by Bottle:

* Rocket
* Waitress
* CherryPy
* Paste

You can find information about these on Bottle's [Deployment][deploy] info page.

All of them except CherryPy had issues. The most important problem, and a showstopper,
is the inability to detect when a client closed the connection (closed the browser window)
and shut down that request thread. The frameworks that fail to do this (Rocket and Waitress)
just keep piling up threads. Some frameworks did stop the thread/request, but did so with
an uncaught exception or exception console spew.

Some frameworks had issues shutting down on Ctrl-C. Rocket would not terminate at all
when one of the threads was still running (and as noted above it was not possible
to stop these threads in Rocket's case) without a kill -9. The paste framework did
shut down, but with an ugly exception.

[bottle]: http://bottlepy.org/docs/dev/
[sse]: http://www.html5rocks.com/en/tutorials/eventsource/basics/
[deploy]: http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend

## Results

Here is an overview of the results:

                                      | wsgiref | rocket | cherrypy | waitress | paste
    ----------------------------------+---------+--------+----------+----------+-------
    stops thread/calling next()       | ok      | -      | ok       | -        | ok
    calls close()                     | -       | -      | ok       | -        | ok
    does not throw or spew            | -       | ok     | ok       | ok       | -
    stops (cleanly) on Ctrl-C         | ok      | -      | ok       | ok       | -
    Properly sends chunks             | ok      | ok     | ok       | -        | ok
    handles concurrent requests       | -       | ok     | ok       | ok       | ok

## Running the tests

To reproduce them, check out this project and start the server like this:

    ./run-test.sh cherrypy

then connect to this URL in your browser, I tested with Safari only:

    http://localhost:8080

You should see output like this slowly getting added:

    event: progress
    data: {"progress": 1, "thread": "<WorkerThread(CP Server Thread-1, started 4489486336)>", "generator": "<__main__.ContentGenerator object at 0x10aefb610>"}

    event: progress
    data: {"progress": 2, "thread": "<WorkerThread(CP Server Thread-1, started 4489486336)>", "generator": "<__main__.ContentGenerator object at 0x10aefb610>"}

When you close the window/tab, the requests in the terminal should stop.

