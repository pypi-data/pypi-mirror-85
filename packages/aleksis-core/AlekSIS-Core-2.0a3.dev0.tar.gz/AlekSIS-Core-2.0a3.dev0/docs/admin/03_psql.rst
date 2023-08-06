Installing AlekSIS with PostgreSQL backend
==========================================

PostgreSQL is the only supported database backend for AlekSIS. If you are
installing AlekSIS manually, you need to properly set it up.

Install the PostgreSQL server
-----------------------------

On Debian, install the postgresql server package with::

  sudo apt install postgresql


Create a database and user
--------------------------

On Debian, you can use the following commands to create the database and a
user who owns it::

  sudo -u postgres createuser -D -P -R -S aleksis
  sudo -u postgres createdb -E UTF-8 -O aleksis -T template0 -l C.UTF-8 aleksis

When asked for the database user password, choose a secure, preferrably
random, password. You can generate one using the pwgen utility if you like::

  pwgen 16 1


Configure AlekSIS to use PostgreSQL
-----------------------------------

Fill in the configuration under `/etc/aleksis/aleksis.toml` (or a file with any other name in this directory)::

  [database]
  host = "localhost"
  name = "aleksis"
  username = "aleksis"
  password = "Y0urV3ryR4nd0mP4ssw0rd"

Don't forget to run the migrations, like described in the basic setup guide.
