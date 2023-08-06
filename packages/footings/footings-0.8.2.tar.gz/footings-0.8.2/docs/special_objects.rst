
Special Objects
===============

Special objects exist within the footings framework that were created to assist in building
models. They are -

- DispatchFunction

These can be created with their representative factory functions - *dispatch_function*.

DispatchFunction
----------------

The DispatchFunction is a useful object to use when you want one generic function to exist that
calls different functions based on passed parameters. This object is similar to the
`singledispatch <https://docs.python.org/3/glossary.html#term-single-dispatch>`_ function built
into the standard library. However, instead of calling a registered function based on the type of an
argument, the function is called based on a passed parameter.

To help users understand the benefit of this object, we will walk through its use continuing
with the DLR example from the user guide. In the DLR model, we have a function called *add_ctr*.
This adds the claim termination rate to the table which is necessary to calculate lives inforce.
This is one function and we might want to call different functions based on whether we
are modeling DLR for statuatory (STAT) reporting, GAAP reporting or modeling a best estimate assumption.

Below is the code to use when creating a *add_ctr* function that calls different functions based on
the reporting needs -

.. code-block:: python

    import pandas as pd
    from footings import dispatch_function

    @dispatch_function(key_parameters=("reporting_type",))
    def add_ctr(reporting_type, frame):
        raise NotImplementedError("No default function is implemented")

    @add_ctr.register(reporting_type="STAT")
    def _(frame):
        frame["CTR"] = 0.02
        return frame

    @add_ctr.register(reporting_type="GAAP")
    def _(frame):
        frame["CTR"] = 0.015
        return frame

    @add_ctr.register(reporting_type="BEST-ESTIMATE")
    def _(frame):
        frame["CTR"] = 0.01
        return frame

    frame = pd.DataFrame({"DURATION": range(1, 5)})

    add_ctr(reporting_type="STAT", frame=frame)
    #   DURATION    CTR
    # 0	1	    0.02
    # 1	2	    0.02
    # 2	3	    0.02
    # 3	4	    0.02

    add_ctr(reporting_type="GAAP", frame=frame)
    #   DURATION    CTR
    # 0	1	    0.015
    # 1	2	    0.015
    # 2	3	    0.015
    # 3	4	    0.015

    add_ctr(reporting_type="BEST-ESTIMATE", frame=frame)
    #   DURATION    CTR
    # 0	1	    0.01
    # 1	2	    0.01
    # 2	3	    0.01
    # 3	4	    0.01

A developer could build this same pattern using an ifelse block within a single function. Though,
using the above pattern is preferable because when the need arises to add a new function, a developer
only needs to register a new function which will minimize the need to change existing blocks of code.
