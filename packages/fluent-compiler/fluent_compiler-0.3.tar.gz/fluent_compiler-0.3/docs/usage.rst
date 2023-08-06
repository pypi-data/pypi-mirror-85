Using fluent_compiler
=====================

Learn the FTL syntax
--------------------

FTL is a localization file format used for describing translation
resources. FTL stands for *Fluent Translation List*.

FTL is designed to be simple to read, but at the same time allows to
represent complex concepts from natural languages like gender, plurals,
conjugations, and others.

::

    hello-user = Hello, { $username }!

In order to use fluent_compiler, you will need to create FTL files. `Read the
Fluent Syntax Guide <http://projectfluent.org/fluent/guide/>`_ in order to
learn more about the syntax.

Using fluent-compiler
---------------------

fluent-compiler has two interfaces for generating messages from FTL files. The
first is :func:`fluent_compiler.compiler.compile_messages`. It's assumed that
most users will want this interface, but will add their own wrappers. Usually
this will provide the best possibilities in terms of performance.

The second interface is :class:`fluent_compiler.bundle.FluentBundle`, which is
slightly higher level. If you use this class directly, it is recommended to
create your own wrapper to insulate your code from any changes in interface we
make. You could also copy its source code as the basis for your own
``compile_messages`` wrapper.

General usage examples below use ``FluentBundle``.


.. _formatting-messages:

Formatting messages
-------------------

Here is how to format messages using the ``FluentBundle`` class.

The ``FluentBundle`` constructor takes a list of :class:`FtlResource` objects as
input, but for convenience there are some alternative constructors
:meth:`~fluent_compiler.bundle.FluentBundle.from_string` and
:meth:`~fluent_compiler.bundle.FluentBundle.from_files`. Both take a locale
string (in BCP 47 format) as a first parameter. To construct from a string:

.. code-block:: python

    >>> from fluent_compiler.bundle import FluentBundle
    >>> bundle = FluentBundle.from_string("en-US", """
    ... welcome = Welcome to this great app!
    ... greet-by-name = Hello, { $name }!
    ... """)


If we had these in a ``my_messages.ftl`` file on disk, we could construct like
this:

.. code-block:: python

    >>> bundle = FluentBundle.from_files("en-US", ["my_messages.ftl"])

To generate translations, use the ``format`` method, passing a message ID and an
optional dictionary of substitution parameters. If the message ID is not found,
a ``LookupError`` is raised. Otherwise, as per the Fluent philosophy, the
implementation tries hard to recover from any formatting errors and generate the
most human readable representation of the value. The ``format`` method therefore
returns a tuple containing ``(translated string, errors)``, as below.

.. code-block:: python

    >>> translated, errs = bundle.format('welcome')
    >>> translated
    "Welcome to this great app!"
    >>> errs
    []

    >>> translated, errs = bundle.format('greet-by-name', {'name': 'Jane'})
    >>> translated
    'Hello, \u2068Jane\u2069!'

    >>> translated, errs = bundle.format('greet-by-name', {})
    >>> translated
    'Hello, \u2068name\u2069!'
    >>> errs
    [FluentReferenceError('Unknown external: name')]

You will notice the extra characters ``\u2068`` and ``\u2069`` in the output.
These are Unicode bidi isolation characters that help to ensure that the
interpolated strings are handled correctly in the situation where the text
direction of the substitution might not match the text direction of the
localized text. These characters can be disabled if you are sure that is not
possible for your app by passing ``use_isolating=False`` to the ``FluentBundle``
constructor.

Python 2
~~~~~~~~

The above examples assume Python 3. Since Fluent uses unicode everywhere
internally (and doesn't accept bytestrings), if you are using Python 2 you will
need to make adjustments to the above example code. Either add ``u`` unicode
literal markers to strings or add this at the top of the module or the start of
your repl session:

.. code-block:: python

    from __future__ import unicode_literals


Numbers
~~~~~~~

When rendering translations, Fluent passes any numeric arguments (``int``,
``float`` or ``Decimal``) through locale-aware formatting functions:

.. code-block:: python

    >>> bundle = FluentBundle.from_string("en", "show-total-points = You have { $points } points.")
    >>> val, errs = bundle.format("show-total-points", {'points': 1234567})
    >>> val
    'You have 1,234,567 points.'

You can specify your own formatting options on the arguments passed in by
wrapping your numeric arguments with ``fluent_compiler.types.fluent_number``:

.. code-block:: python

    >>> from fluent_compiler.types import fluent_number
    >>> points = fluent_number(1234567, useGrouping=False)
    >>> bundle.format("show-total-points", {'points': points})[0]
    'You have 1234567 points.'

    >>> amount = fluent_number(1234.56, style="currency", currency="USD")
    >>> bundle = FluentBundle.from_string("en", "your-balance = Your balance is { $amount }")
    >>> bundle.format("your-balance", {'amount': amount})[0]
    'Your balance is $1,234.56'

The options available are defined in the Fluent spec for `NUMBER
<https://projectfluent.org/fluent/guide/functions.html#number>`_. Some of these
options can also be defined in the FTL files, as described in the Fluent spec,
and the options will be merged.

Date and time
~~~~~~~~~~~~~

Python ``datetime.datetime`` and ``datetime.date`` objects are also
passed through locale aware functions:

.. code-block:: python

    >>> from datetime import date
    >>> bundle = FluentBundle.from_string("en", "today-is = Today is { $today }")
    >>> val, errs = bundle.format("today-is", {"today": date.today() })
    >>> val
    'Today is Jun 16, 2018'

You can explicitly call the ``DATETIME`` builtin to specify options:

.. code-block:: python

    >>> FluentBundle.from_string('en', 'today-is = Today is { DATETIME($today, dateStyle: "short") }')

See the `DATETIME docs
<https://projectfluent.org/fluent/guide/functions.html#datetime>`_. However,
currently the only supported options to ``DATETIME`` are:

- ``timeZone``
- ``dateStyle`` and ``timeStyle`` which are `proposed additions
  <https://github.com/tc39/proposal-ecma402-datetime-style>`_ to the ECMA i18n
  spec.

To specify options from Python code, use
``fluent_compiler.types.fluent_date``:

.. code-block:: python

    >>> from fluent_compiler.types import fluent_date
    >>> today = date.today()
    >>> short_today = fluent_date(today, dateStyle='short')
    >>> val, errs = bundle.format("today-is", {"today": short_today })
    >>> val
    'Today is 6/17/18'

You can also specify timezone for displaying ``datetime`` objects in two ways:

- Create timezone aware ``datetime`` objects, and pass these to the ``format``
  call e.g.:

  .. code-block:: python

      >>> import pytz
      >>> from datetime import datetime
      >>> utcnow = datime.utcnow().replace(tzinfo=pytz.utc)
      >>> moscow_timezone = pytz.timezone('Europe/Moscow')
      >>> now_in_moscow = utcnow.astimezone(moscow_timezone)

- Or, use timezone naive ``datetime`` objects, or ones with a UTC
  timezone, and pass the ``timeZone`` argument to ``fluent_date`` as a
  string:

  .. code-block:: python

      >>> utcnow = datetime.utcnow()
      >>> utcnow
      datetime.datetime(2018, 6, 17, 12, 15, 5, 677597)

      >>> bundle = FluentBundle("en", "now-is = Now is { $now }")
      >>> val, errs = bundle.format("now-is",
      ...    {"now": fluent_date(utcnow,
      ...                        timeZone="Europe/Moscow",
      ...                        dateStyle="medium",
      ...                        timeStyle="medium")})
      >>> val
      'Now is Jun 17, 2018, 3:15:05 PM'


Known limitations and bugs
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Most options to ``DATETIME`` are not yet supported. See the `MDN docs for
  Intl.DateTimeFormat
  <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DateTimeFormat>`_,
  the `ECMA spec for BasicFormatMatcher
  <http://www.ecma-international.org/ecma-402/1.0/#BasicFormatMatcher>`_ and the
  `Intl.js polyfill
  <https://github.com/andyearnshaw/Intl.js/blob/master/src/12.datetimeformat.js>`_.

Help with the above would be welcome!

Be sure to check the notes on :doc:`implementations`, especially the security
section.


Other features and further information
--------------------------------------

* :doc:`functions`
* :doc:`errors`
* :doc:`escaping`
* :doc:`security`
* :doc:`implementations`
