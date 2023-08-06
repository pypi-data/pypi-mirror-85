.. _changelog:

==========
Change Log
==========

All notable changes to this project will be documented here.

Sort subsections like so: Added, Bugfixes, Improvements, Technical tasks.
Group anything an end user shouldn't care deeply about into technical
tasks, even if they're technically bugs. Only include as "bugfixes"
bugs with user-visible outcomes.

When major components get significant changes worthy of mention, they
can be described in a Major section.

More information can be found `HERE <https://keepachangelog.com/en/1.0.0/>`__:


v0.1.0 - 2020-11-18
===================

Major
-----

* Moved cLRU code to it's own repo

Technical Tasks
---------------

* Added Github Action hook to run the tests for every PR
* Added the imports on the ``__init__.py`` to import the cython version when
  possible
