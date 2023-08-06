AlekSIS — All-libre extensible kit for school information systems
=================================================================

Warning
-------

**This is an alpha version of AlekSIS, the free school information system.
The AlekSIS team is looking for schools who want to help shape the 2.0
final release and supports interested schools in operating AlekSIS.**

What AlekSIS is
----------------

`AlekSIS`_ is a web-based school information system (SIS) which can be used to
manage and/or publish organisational subjects of educational institutions.

Formerly two separate projects (BiscuIT and SchoolApps), developed by
`Teckids e.V.`_ and a team of students at `Katharineum zu Lübeck`_, they
were merged into the AlekSIS project in 2020.

AlekSIS is a platform based on Django, that provides central funstions
and data structures that can be used by apps that are developed and provided
seperately. The AlekSIS team also maintains a set of official apps which
make AlekSIS a fully-featured software solutions for the information
management needs of schools.

By design, the platform can be used by schools to write their own apps for
specific needs they face, also in coding classes. Students are empowered to
create real-world applications that bring direct value to their environment.

AlekSIS is part of the `schul-frei`_ project as a component in sustainable
educational networks.

Core features
--------------

* For users:

 * Custom menu entries (e.g. in footer)
 * Global preferences
 * Group types
 * Manage announcements
 * Manage groups
 * Manage persons
 * Notifications via SMS email or dashboard
 * Rules and permissions for users, objects and pages
 * Two factor authentication via Yubikey, OTP or SMS
 * User preferences

* For admins

 * Asynchronous tasks with celery
 * Authentication via LDAP
 * Automatic backup of database, static and media files

Official apps
-------------

+--------------------------------------+---------------------------------------------------------------------------------------------+
| App name                             | Purpose                                                                                     |
+======================================+=============================================================================================+
| `AlekSIS-App-Chronos`_               | The Chronos app provides functionality for digital timetables.                              |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-DashboardFeeds`_        | The DashboardFeeds app provides functionality to add RSS or Atom feeds to dashboard         |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Hjelp`_                 | The Hjelp app provides functionality for aiding users.                                      |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-LDAP`_                  | The LDAP app provides functionality to import users and groups from LDAP                    |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Untis`_                 | This app provides import and export functions to interact with Untis, a timetable software. |
+--------------------------------------+---------------------------------------------------------------------------------------------+


Licence
-------

::

  Copyright © 2017, 2018, 2019, 2020 Jonathan Weth <wethjo@katharineum.de>
  Copyright © 2017, 2018, 2019 Frank Poetzsch-Heffter <p-h@katharineum.de>
  Copyright © 2018, 2019, 2020 Julian Leucker <leuckeju@katharineum.de>
  Copyright © 2018, 2019, 2020 Hangzhi Yu <yuha@katharineum.de>
  Copyright © 2019, 2020 Dominik George <dominik.george@teckids.org>
  Copyright © 2019, 2020 Tom Teichler <tom.teichler@teckids.org>
  Copyright © 2019 mirabilos <thorsten.glaser@teckids.org>

  Licenced under the EUPL, version 1.2 or later

Please see the LICENCE.rst file accompanying this distribution for the
full licence text or on the `European Union Public Licence`_ website
https://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers
(including all other official language versions).

.. _AlekSIS: https://aleksis.org/
.. _Teckids e.V.: https://www.teckids.org/
.. _Katharineum zu Lübeck: https://www.katharineum.de/
.. _European Union Public Licence: https://eupl.eu/
.. _schul-frei: https://schul-frei.org/
.. _AlekSIS-App-Chronos: https://edugit.org/AlekSIS/official/AlekSIS-App-Chronos
.. _AlekSIS-App-DashboardFeeds: https://edugit.org/AlekSIS/official/AlekSIS-App-DashboardFeeds
.. _AlekSIS-App-Hjelp: https://edugit.org/AlekSIS/official/AlekSIS-App-Hjelp
.. _AlekSIS-App-LDAP: https://edugit.org/AlekSIS/official/AlekSIS-App-LDAP
.. _AlekSIS-App-Untis: https://edugit.org/AlekSIS/official/AlekSIS-App-Untis
