=================
Kelvin API Client
=================

Im letzten Sprint hat das UCS\@school Team einen Python Client für die `UCS\@school Kelvin REST API <https://docs.software-univention.de/ucsschool-kelvin-rest-api/>`_ veröffentlicht[#]_.
Zur Erinnerung: Ziel der Kelvin API ist es, über HTTP-Befehle alle UCS@school Objekte editierbar zu machen.
Implementiert wurden bisher aber nur die für andere Projekte wichtigen Typen ("Ressourcen") ``User``, ``Role``, ``School`` und ``School Class``.

Motivation
----------

Nutzer ("Clients") der Kelvin API müssen sich für den Zugriff auf die Ressourcen einen Session-Schlüssel ("Token") besorgen[#]_.
Da dieser zeitlich begrenzt ist, müssen sie ihn regelmäßig erneuern.
Die Länge der Gültigkeit ist serverseitig einstellbar.
D.h. der Client muss den `JSON Web Token (JWT) <https://en.wikipedia.org/wiki/JSON_Web_Token>`_ parsen und die Erneuerung entsprechend planen.

Empfangene und zu sendende Daten in so einer HTTP API haben bestimmtes Format und Encoding, ebenso die Fehlermeldungen.
Clients müssen dies bei der Benutzung beachten.
Dies ist zwar alles schön dokumentiert, aber es macht natürlich wenig Sinn, dass jede_r Programmierer_in die die API nutzen möchte, sich damit erneut auseinander setzt und ähnlichen Code wieder und wieder scheibt und diesen auch noch schwer wartbar überall verstreut.

Deswegen haben wir eine kleine Programmierbibliothek ("library") geschrieben, die Programmierer_innen dies abnimmt, und in der Verbesserungen für alle an zentraler Stelle einfließen können.

API Design
----------

Diese library - der `Python UCS\@school Kelvin REST API Client <https://github.com/univention/kelvin-rest-api-client>`_) - kann und muss (wie jede Software) wiederum auf eine bestimmte Art und Weise verwendet werden - hat also selbst eine API.

Bei dem Design dieser API habe ich mich an dem des `UDM REST API Clients <https://hutten.knut.univention.de/blog/modernes-oeffentliches-open-source-python-projekt/>` orientiert.
Dies sollte Anwendern selbiger den Einstieg in die neue API erleichtern.

Wie der *UDM REST API Client* belästigt der *Kelvin REST API Client* einen nicht mit unnötigen Details.
So gibt es keine Methoden ``create()``, ``modify()`` und ``move()``, sondern nur ``save()``.
Es ist Aufgabe des Servers und des Clients das Richtige daraus zu machen.

Die Methoden können aneinander gereiht ("chained") werden, es entsteht eine sog. "fluid API".
D.h. es kann so etwas ausgeführt werden: ``obj.save().reload().delete()`` (auch wenn das Beipiel wenig Sinn macht:).

Da das Öffnen vom HTTP(S)-Verbindungen recht teuer ist, wird die gleiche HTTP-Session für mehrere Kommandos zusammen verewndet.
Das Nicht-Schließen von HTTP-Session ist aber ebenfalls teuer, und darüber hinaus muss die Laufzeit des Tokens beachtet werden.
Deswegen bietet auch diese Client API einen ContextManager an, welcher das alles für einen erledigt.

Da HTTP-Zugriffe im Vergleich zu LDAP-Zugriffen aufwändig und langsam sind, bietet die API asynchrone Methoden (``async/await``) an.
Dies ermöglicht diese prinzipbedingten Nachteile durch Parallelität im Client-Code zu kompensieren.

Installation
------------

.. code-block:: shell

    $ pip install kelvin-rest-api-client

Python
------

* Die Software läuft (und wird getestet) unter Python 3.7, 3.8 und 3.9.
* Statische Analyse wird unterstützt dank durchgehender Verwendung von *type annotations*.

Beispiele
---------

Zugangsdaten:

.. code-block:: python

    credentials = {
        "username": "Administrator",
        "password": "s3cr3t",
        "host": "master.ucs.local",
        "verify": "ucs-root-ca.pem",
    }

Suchen nach Schulklassen:

.. code-block:: python

    from ucsschool.kelvin.client import Session, SchoolClassResource

    async with Session(**credentials) as session:
        async for sc in SchoolClassResource(session=session).search(school="DEMOSCHOOL"):
            print(sc)

    SchoolClass('name'='Democlass', 'school'='DEMOSCHOOL', dn='cn=DEMOSCHOOL-Democlass,cn=klassen,cn=schueler,cn=groups,ou=DEMOSCHOOL,dc=example,dc=com')
    SchoolClass('name'='testclass', 'school'='DEMOSCHOOL', dn='cn=DEMOSCHOOL-testclass,cn=klassen,cn=schueler,cn=groups,ou=DEMOSCHOOL,dc=example,dc=com')

Erstellen eines neuen Users:

.. code-block:: python

    from ucsschool.kelvin.client import Session, User

    async with Session(**credentials) as session:
        user = User(
            school="DEMOSCHOOL",
            schools=["DEMOSCHOOL"],
            roles=["student"],
            name="test1",
            firstname="test",
            lastname="one",
            record_uid="test1",
            source_uid="TESTID",
            session=session
        )
        await user.save()

    user.dn
    'uid=test1,cn=schueler,cn=users,ou=DEMOSCHOOL,dc=example,dc=com'

Ändern eines Users:

.. code-block:: python

    from ucsschool.kelvin.client import Session, UserResource

    async with Session(**credentials) as session:
        user = await UserResource(session=session).get(name="demo_student")
        user.firstname = "Peter"
        user.lastname = "Lustig"
        user.password = "password123"
        await user.save()

Löschen eines Users:

.. code-block:: python

    from ucsschool.kelvin.client import Session, UserResource

    async with Session(**credentials) as session:
        await UserResource(session=session).get(name="demo_student").delete()


Dokumentation
-------------

Die Dokumentation für den Kelvin API Client wurde auf Read the Docs (RTD) veröffentlicht: https://kelvin-rest-api-client.readthedocs.io/

Dort finden sich neben Informationen über Installation, Tests und Logging je ein Kapitel pro Ressource mit der Bespreibung der Klassen, ihrer Attribute und Methoden, sowie je einem Beipiel pro Methode.
Zum Beispiel `School Class <https://kelvin-rest-api-client.readthedocs.io/en/latest/usage-school-class.html>`_.

Linting
-------

Wie in allen unseren Nicht-Debian-Paket-Projekten setzen wir jetzt immer einen konsistenten Code Stil durch.

Dieser wird nun auch vor dem Commiten mit mehreren pre-commit-Hooks erzwungen.
Dazu mehr in einem anderen Blogeintrag.

Zum Einsatz kommen hier:

* `black <https://github.com/psf/black>`_: PEP8-konforme Formatierung
* `isort <https://github.com/timothycrosley/isort>`_: Imports-Sortierung
* `flake8 <https://gitlab.com/pycqa/flake8>`_: diverse Code Qualitäten
* `bandit <https://github.com/PyCQA/bandit>`_: security scanner
* diverse Linter für JSON, MD, RST, XML, YAML, requirements.txt, safety-db...

Tests, CI, Coverage
-------------------

Eine ``pytest`` verwendende Testsuite prüft die Funktionalität.

Bei jedem push ins Git Repository wird automatisch eine VM bei Travis CI gestartet, die die Tests mit ``tox`` für alle unterstützten Python Versionen (3.7, 3.8 und 3.9) durchführt: https://travis-ci.com/univention/kelvin-rest-api-client
Damit die Tests dort laufen können wurden Docker Container mit UCS\@school erstellt (siehe unten).

Die dabei gemessene Code Coverage (z.Z. 97%) wird automatisch zu Codecov hochgeladen: https://codecov.io/gh/univention/kelvin-rest-api-client

Die Testsuite unterstützt sowohl die Nutzung eines eigenen UCS Systems (Daten in YAML Datei schreiben) als auch Docker Container (Daten werden automatisch ausgelesen).

Docker container
^^^^^^^^^^^^^^^^

Für die Integrationstests wird ein laufendes UCS mit dem UDM REST API Server, konfiguriertem UCS\@school Master und dem Kelvin API Server benötigt.

Tests (und bei Integrationstests die Umgebungen) sollten reproduzierbar sein, auf dem Entwicklergerät und bei Travis CI laufen können.
Dazu sollte alles in Docker Container verpackt werden.
Und am Ende muss alles mit einem Befehl gestartet werden können (Einfachheit für Entwickler und für's Deployment bei Travis).
Und natürlich soll es möglichst zügig starten - also so viel wie möglich beim Imagebau passieren, und möglich wenig beim Containerstart.
Das war eine ziemliche Herausforderung!

Für die Tests der UDM REST API hatte ich bereits, mit Tricks über docker-compose, einen Docker Container mit einem bereits gejointem UCS erzeugt, welcher nur OpenLDAP, Apache und die UDM REST API startet.
In diesen Container musste also noch UCS\@school installiert und als Singlemaster konfiguriert werden.
Außerdem musste die Kelvin API App installiert werden.
Die Kelvin API App ist jedoch eine Docker App.
Und Docker Container lassen sich nicht ohne weiteres in Docker Containern starten.

Funktionieren tut es nun folgendermaßen:

* Beim Bau des Images installiert und konfiguriert der UCS Container nun UCS\@school, so wie wir es in Jenkins tun.
* Anschließend führt er die relevanten Teile des Join Skripts der Kelvin API App aus, um später die Authentifizierung an dieser zu ermöglichen.
* Zum Schluss wird noch OpenRC in das UCS installiert, so dass beim Starten des Containers nur OpenLDAP, NSCD, Apache und die UDM REST API starten.
* Das Makefile startet den UCS Container und wartet auf die Verfügbarkeit der UDM REST API.
* Ein temporärer Kelvin API Container wird nun erzeugt, aber nicht gestartet. Aus ihm werden einige Konfigurationsdateien des ucs-school-import kopiert. Der temporäre Container wird dann wieder gelöscht.
* Ein weiterer Kelvin API Container wird nun erzeugt, ebenfalls nicht gestartet. In ihn hinein wird eine ganze Reihe Dateien kopiert: UCR-Datenbank mit LDAP-Daten des Masters/der Domäne, Machine- und cn=admin-Secret aus dem UCS-Container, CA-Zertifikat aus dem UCS-Container, Import-Config, Token-Secret (aus dem App Join Script).
* Das Makefile startet den Kelvin Container, konfiguriert ihn noch etwas und wartet dann auf die Verfügbarkeit der Kelvin API.

Der Bau des UCS\@school Images dauert auf meinem Notebook etwa 50 Minuten, es wird 2,8 GB groß.
Auf Univentions Docker build/registry Host kann es leider nicht gebaut werden, weil das ``docker-compose`` auf dem System zu alt ist (UCS 4.3-5).
Ich uploade es daher von meinem Notebook dorthin und pushe es dann in die Test-Registry.
Wenn ihr oder Travis CI es nutzen wollen, so braucht ihr es also nicht mehr zu bauen.
Es steht bereits als::

    docker-test.software-univention.de/ucs-master-amd64-joined-ucsschool-udm-rest-api-only:stable-4.4-4

Das Start der Container sieht in etwa so aus:

.. code-block:: shell

    $ make start-docker-containers

    Downloading Docker image '..-ucsschool-udm-rest-api-only:stable-4.4-4'...
    Downloading Docker image '../ucsschool-kelvin-rest-api:1.1.0'...
    Starting UCS docker container...
    Waiting for UCS docker container to start...
    Waiting for IP address of UCS container...
    Waiting for UDM REST API...........
    Creating Kelvin REST API container...
    Configuring Kelvin REST API container...
    Rebuilding the OpenAPI client library in the Kelvin API Container...
    Starting Kelvin REST API server...
    Waiting for Kelvin docker container to start...
    Waiting for IP address of Kelvin container...
    Waiting for Kelvin API...
    Fixing log file permissions...
    Setting up reverse proxy...
    ==> UDM REST API log file: /tmp/udm-rest-api-log/directory-manager-rest.log
    ==> UDM REST API: http://172.17.0.2/univention/udm/
    ==> Kelvin API configs: /tmp/kelvin-api/configs/
    ==> Kelvin API hooks: /tmp/kelvin-api/kelvin-hooks/
    ==> Kelvin API log file: /tmp/kelvin-api/log/http.log
    ==> Kelvin API: http://172.17.0.3:8911/ucsschool/kelvin/v1/docs
    ==> Kelvin API: https://172.17.0.2/ucsschool/kelvin/v1/docs

Der Start der beiden Container dauert auf meinem Notebook 40-60 Sekunden.
Sie brauchen zusammen etwa 500 MB RAM.

Anschließend können die Tests ohne weitere Konfiguration gestartet werden.
Sie laufen auf meinem Notebook etwa 2 Minuten lang.

Links
-----

* Repo auf internem Gitlab: https://git.knut.univention.de/univention/components/kelvin-rest-api-client
* Repo auf Github: https://github.com/univention/kelvin-rest-api-client
* Documentation: https://kelvin-rest-api-client.readthedocs.io
* Tests (Travis CI): https://travis-ci.com/univention/kelvin-rest-api-client
* Coverage: https://codecov.io/gh/univention/kelvin-rest-api-client


.. [#] Auf Grund von Umplanungen wurde der Code bereits veröffentlicht, aber noch nicht QAt.
.. [#] https://docs.software-univention.de/ucsschool-kelvin-rest-api/authentication-authorization.html
