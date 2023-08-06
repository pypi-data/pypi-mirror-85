iva2k_how_long
==============

Simple Decorator to measure a function execution time.

Very lightweight project to get familiar with poetry publishing to PyPi, built from tutorial https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1


Example
_______

.. code-block:: python

    from iva2_how_long import timer


    @timer
    def some_function():
        return [x for x in range(10_000_000)]
        