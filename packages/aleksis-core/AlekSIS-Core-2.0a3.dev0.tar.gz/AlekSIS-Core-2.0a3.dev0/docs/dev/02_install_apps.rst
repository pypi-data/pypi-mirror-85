Installing apps into development environment
============================================

Officially bundled apps
-----------------------

Officially bundlede apps are available in the ``apps/official/``
sub-folder as Git submodules. If you followed the documentation, they
will already be checked out in the version required for the bundle you
are running.

Installing apps into the existing virtual environment is a bit awkward::

  poetry run sh -c "cd apps/official/AlekSIS-App-Exlibris; poetry install"

This will install the Exlibris app (library management) app by using a
shell for first ``cd``'ing into the app directory and then using
poetry to install the app.

Do not forget to run the maintenance tasks described earlier after
installing any app.
