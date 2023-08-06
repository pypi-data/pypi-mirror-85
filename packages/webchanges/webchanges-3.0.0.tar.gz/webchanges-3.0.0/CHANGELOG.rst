*********
Changelog
*********

This changelog mostly follows `keep a changelog <https://keepachangelog.com/en/1.0.0/>`__. Release numbering mostly
follows `Semantic Versioning <https://semver.org/spec/v2.0.0.html#semantic-versioning-200>`__.

Unreleased
==========

Development
-----------
* Upgraded Travis CI to Python 3.9 from 3.9-dev and cleaned up pip installs
* Added Python nightly to Travis CI

`Contributions <https://github.com/mborsetti/webchanges/blob/master/CONTRIBUTING.rst>`__ always welcomed, and you can
check out the `wish list <https://github.com/mborsetti/webchanges/blob/master/WISHLIST.rst>`__ for inspiration.

Unreleased versions can be installed as follows:

.. code-block:: bash

   pip install git+https://github.com/mborsetti/webchanges.git@unreleased

Note: git needs to be `installed <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__ for this to work.


Version 3.0.0
=============
2020-11-12

Milestone
---------
Initial release of `webchanges` as a reworked fork of `urlwatch` 2.21. Changes below are relative to `urlwatch` 2.21

Added
-----
* You can now specify just a ``url`` and the "just works for web" philosophy optimizes the monitoring of text in
  webpages by applying all necessary filters  **TODO**
* If no job ``name`` is provided, the title of an HTML page will be used for a job name in reports
* The Python ``html2text`` package (used by the ``html2text`` filter, previously known as ``pyhtml2text``) is now
  initialized with the following purpose-optimized non-default `options
  <https://github.com/Alir3z4/html2text/blob/master/docs/usage.md#available-options>`__: unicode_snob = True,
  body_width = 0, single_line_break = True, and ignore_images = True
* The output from ``html2text`` filter is reconstructed into HTML (for html reports), preserving basic formatting
  such as bolding, italics, list bullets, etc. as well as making links clickable
* HTML formatting is radically more legible and useful, including long lines wrapping around
* HTML formatting uses color (green or red) and strikethrough to mark added and deleted lines
* HTML reports are now rendered correctly by email clients who reformat stylesheets (e.g. Gmail)
* Filter ``format-xml`` reformats (pretty-prints) XML
* ``webchanges --errors`` will run all jobs and list all errors and empty responses (after filtering)
* Browser jobs now recognize ``cookies``, ``headers``, ``http_proxy``, ``https_proxy``, and ``timeout`` sub-directives
* The revision number of Chromium browser to use can be selected with ``chromium_revision``
* Can set the user directory for the Chromium browser with ``user_data_dir``
* Chromium can be directed to ignore HTTPs errors with ``ignore_https_errors``
* Chromium can be directed as to when to consider a page loaded with ``wait_until``
* Additional command line switches can be passed to Chromium with ``switches``
* New report filters ``additions_only`` and ``deletions_only`` allow to track only content that was added (or
  deleted) from the source
* Support for Python 3.9
* Backward compatibility with `urlwatch` 2.21 (except running on Python 3.5 or using ``lynx``, which is replaced by
  internal ``html2text`` filter)

Changed and deprecated
----------------------
* Navigation by full browser is now accomplished by specifying the ``url`` and adding the ``use_browser: true``
  directive. The `navigate` directive has been deprecated for clarity and will trigger a warning ***TODO***
* The name of the default program configuration file has been changed to ``config.yaml``; if at program launch
  ``urlwatch.yaml`` is found and no ``config.yaml`` exists, it is copied over for backward-compatibility.
* In Windows, the location of config files has been moved to ``%USERPROFILE%\Documents\webchanges``
  where they can be more easily edited (they are indexed there) and backed up
* The ``html2text`` filter defaults to using the Python ``html2text`` package (with optimized defaults) instead of
  ``re``
* New `additions_only` directive to report only added lines (useful when monitoring only new content)
* New `deletions_only` directive to report only deleted lines
* `keyring` Python package is no longer installed by default
* `html2text` and `markdown2` Python packages are installed by default
* Installation of Python packages required by a feature is now made easier with pip extras (e.g. ``pip install -U
  webchanges[ocr,pdf2text]``)
* The name of the default job's configuration file has been changed to ``jobs.yaml``; if at program launch ``urls.yaml``
  is found and no ``jobs.yaml`` exists, it is copied over for backward-compatibility
* The ``html2text`` filter's ``re`` method has been renamed ``strip_tags``, which is deprecated and will trigger a
  warning
* The ``grep`` filter has been renamed ``keep_lines_containing``, which is deprecated and will trigger a warning
* The ``grepi`` filter has been renamed ``delete_lines_containing``, which is deprecated and will trigger a warning
* Both the ``keep_lines_containing`` and ``delete_lines_containing`` accept ``text`` (default) in addition to ``re``
  (regular expressions)
* ``--test`` command line switch is used to test a job (formerly ``--test-filter``, deprecated)
* ``--test-diff`` command line switch is used to test a jobs' diff (formerly ``--test-diff-filter``, deprecated)
* ``-V`` command line switch added as an alias to ``--version``
* If a filename for ``--jobs``, ``--config`` or ``--hooks`` is supplied without a path and the file is not present in
  the current directory, `webchanges` now looks for it in the default configuration directory
* If a filename for ``--jobs`` or ``--config`` is supplied without a '.yaml' suffix, `webchanges` now looks for one with
  such a suffix
* In Windows, ``--edit`` defaults to using built-in notepad.exe if %EDITOR% or %VISUAL% are not set
* When using ``--job`` command line switch, if there's no file by that name in the specified directory will look in
  the default one before giving up.
* The use of the ``kind`` directive in ``jobs.yaml`` configuration files has been deprecated (but is, for now, still
  used internally)
* The ``slack`` webhook reporter allows the setting of maximum report length (for, e.g., usage with Discord) using the
  ``max_message_length`` sub-directive
* The database (cache) file is backed up at every run to `*.bak`
* The mix of default and optional dependencies has been updated (see documentation) to enable "Just works"
* Dependencies are now specified as PyPi `extras
  <https://stackoverflow.com/questions/52474931/what-is-extra-in-pypi-dependency>`__ to simplify their installation
* Changed timing from `datetime <https://docs.python.org/3/library/datetime.html>`__ to `timeit.default_timer
  <https://docs.python.org/3/library/timeit.html#timeit.default_timer>`__
* Upgraded concurrent execution loop to `concurrent.futures.ThreadPoolExecutor.map
  <https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.map>`__
* Reports' elapsed time now always has at least 2 significant digits
* Expanded (only slightly) testing
* Using flake8 to check PEP-8 compliance and more
* Using coverage to check unit testing coverage

Removed
-------
* The ``html2text`` filter's ``lynx`` method is no longer supported; use ``html2text`` instead
* Python 3.5 (obsoleted by 3.6 on December 23, 2016) is no longer supported

Fixed
-----
* The ``html2text`` filter's ``html2text`` method defaults to unicode handling
* HTML href links ending with spaces are no longer broken by ``xpath`` replacing spaces with `%20`
* Initial config file no longer has directives sorted alphabetically, but are saved logically (e.g. 'enabled' is always
  the first sub-directive)
* The presence of the ``data`` directive in a job would force the method to POST preventing PUTs

Security
--------
* None

Documentation changes
---------------------
* Complete rewrite of the documentation

Known bugs
----------
* Documentation could be more complete
* Almost complete lack of inline docstrings in the code
