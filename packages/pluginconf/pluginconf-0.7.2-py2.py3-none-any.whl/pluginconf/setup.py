# encoding: utf-8
# api: setuptools
# type: functions
# title: setup() wrapper
# description: utilizes PMD to populate some package fields
# version: 0.2
# license: PD
#
# Utilizes plugin meta data to cut down setup.py incantations
# to basically just:
#
#     from pluginconf.setup import setup
#     setup(
#         fn="pluginconf/__init__.py",
#         long_description="@README.rst"
#     )
#
# Where the fn= either pinpoints the main invocation point,
# when name= or packages= (implicitly from `find_packages()`)
# don't specify a locatable script already.
#
# Mapped meta fields include:
#
#     # description: …
#     # version: …
#     # url: …
#     # depends: python (>= 2.7), python:pkg-name (>= 1.0)
#     # suggests: python:extras_require (>= 1.0)
#     # author: …
#     # license: spdx
#     # state: stable
#     # type: classifier
#     # category: classifier
#     # keywords: tag, tag
#     # classifiers: tag, trove, shortcuts
#    
# A long_description=README.* will be read automatically,
# else the default PMD comment gets used.
# Classifiers and license matching is very crude, just for
# the most common cases.
#


import os, re
import setuptools
import pluginconf


def setup(**kwargs):
    """
        Wrapper around `setuptools.setup()` which adds some defaults
        and plugin meta data import, with two shortcut params:
        
          fn="pkg/main.py",
          long_description="@README.md"

        Other setup() params work as usual.
    """

    # stub values
    stub = {
        "classifiers": [],
        "project_urls": {},
        "python_requires": ">= 2.7",
        "install_requires": [],
        "extras_require": {},
        #"package_dir": {"": "."},
        "package_data": {},
        "data_files": [],
        "entry_points": {},
        "packages": setuptools.find_packages()
    }
    for k,v in stub.items():
        if not k in kwargs:
            kwargs[k] = v

    # package name
    if not "name" in kwargs:
        kwargs["name"] = kwargs["packages"][0]

    # read README
    if re.match("^@?(./)?README.(\w+)$", kwargs.get("long_description", "-")):
        #system("pandoc -f markdown -t rst README.md  > README.rst")
        kwargs["long_description_content_type"] = "text/x-rst" if re.search("rst", kwargs["long_description"]) else "text/markdown"
        kwargs["long_description"] = open(kwargs["long_description"], "r").read()

    # search name= package if no fn= given
    if not kwargs.get("fn") and kwargs.get("name"):
        name = kwargs["name"]
        ls = (name+"/"+name+".py", name+".py", name+"/__init__py")
        for fn in ls:
            if os.path.exists(fn):
                kwargs["fn"] = fn

    # read plugin meta data (PMD)  
    pmd = {}
    pmd = pluginconf.plugin_meta(fn=kwargs["fn"])
    
    # id: if no name= still
    if pmd.get("id") and not kwargs.get("name"):
        if pmd["id"] == "__init__":
            pmd["id"] = re.findall("([\w\.\-]+)/__init__.+$", kwargs["fn"])[0]
        kwargs["name"] = pmd["id"]
    # cleanup
    if "fn" in kwargs:
        del kwargs["fn"]

    # version:, description:, author:
    for field in "version", "description", "license", "author", "url":
        if field in pmd and not field in kwargs:
            kwargs[field] = pmd[field]
    # other urls:
    for k,url in pmd.items():
        if type(url) is str and k != "url" and re.match("https?://\S+", url):
            kwargs["project_urls"][k.title()] = url
    # depends:
    if "depends" in pmd:
        deps = re.findall("python\s*\(?(>=?\s?[\d.]+)", pmd["depends"])
        if deps:
            kwargs["python_requires"] = deps[0]
    if "depends" in pmd and not kwargs["install_requires"]:
        deps = re.findall("(?:python|pip):([\w\-]+)", pmd["depends"])
        if deps:
            kwargs["install_requires"] = deps
    # suggests:
    if "suggests" in pmd and not kwargs["extras_require"]:
        deps = re.findall("(?:python|pip):([\w\-]+)\s*\(?\s*([>=<]+\s*[\d.\-]+)", pmd["suggests"])
        if deps:
            kwargs["extras_require"].update(dict(deps))
    # doc:
    if not "long_description" in kwargs:
        kwargs["long_description"] = pmd["doc"]
        kwargs["long_description_content_type"] = "text/plain"
    # keywords=
    if not "keywords" in kwargs:
        if "keywords" in pmd:
            kwargs["keywords"] = pmd["keywords"]
        elif "category" in pmd:
            kwargs["keywords"] = pmd["category"]

    # classifiers=
    trove_map = {
        "license": {
            "MITL?": "License :: OSI Approved :: MIT License",
            "PD|Public Domain": "License :: Public Domain",
            "ASL": "License :: OSI Approved :: Apache Software License",
            "art": "License :: OSI Approved :: Artistic License",
            "BSDL?": "License :: OSI Approved :: BSD License",
            "CPL": "License :: OSI Approved :: Common Public License",
            "AGPL.*3": "License :: OSI Approved :: GNU Affero General Public License v3",
            "AGPLv*3\+": "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            "GPL": "License :: OSI Approved :: GNU General Public License (GPL)",
            "GPL.*3": "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "LGPL": "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            "MPL": "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Pyth": "License :: OSI Approved :: Python Software Foundation License"
        },
        "state": {
            "pre|release|cand": "Development Status :: 2 - Pre-Alpha",
            "alpha": "Development Status :: 3 - Alpha",
            "beta": "Development Status :: 4 - Beta",
            "stable": "Development Status :: 5 - Production/Stable",
            "mature": "Development Status :: 6 - Mature"
        }
    }
    # license:
    if pmd.get("license") and not any(re.match("License ::", l) for l in kwargs["classifiers"]):
        for rx,trove in trove_map["license"].items():
            if re.search(rx, pmd["license"], re.I):
                kwargs["classifiers"].append(trove)
    # state:
    if pmd.get("state", pmd.get("status")) and not any(re.match("Development Status ::", l) for l in kwargs["classifiers"]):
        for rx,trove in trove_map["state"].items():
            if re.search(rx, pmd.get("state", pmd.get("status", "stable")), re.I):
                kwargs["classifiers"].append(trove)
    # topics::
    rx = "|".join(re.findall("(\w{4,})", " | ".join([pmd.get(f, "-") for f in ("api", "category", "type", "keywords", "classifiers")])))
    for line in topic_trove:
        if re.search("::[^:]*("+rx+")[^:]*$", line, re.I):
            if line not in kwargs["classifiers"]:
                kwargs["classifiers"].append(line)

    # handover
    setuptools.setup(**kwargs)



topic_trove="""Topic :: Adaptive Technologies
Topic :: Artistic Software
Topic :: Communications
Topic :: Communications :: BBS
Topic :: Communications :: Chat
Topic :: Communications :: Chat :: ICQ
Topic :: Communications :: Chat :: Internet Relay Chat
Topic :: Communications :: Chat :: Unix Talk
Topic :: Communications :: Conferencing
Topic :: Communications :: Email
Topic :: Communications :: Email :: Address Book
Topic :: Communications :: Email :: Email Clients (MUA)
Topic :: Communications :: Email :: Filters
Topic :: Communications :: Email :: Mail Transport Agents
Topic :: Communications :: Email :: Mailing List Servers
Topic :: Communications :: Email :: Post-Office
Topic :: Communications :: Email :: Post-Office :: IMAP
Topic :: Communications :: Email :: Post-Office :: POP3
Topic :: Communications :: FIDO
Topic :: Communications :: Fax
Topic :: Communications :: File Sharing
Topic :: Communications :: File Sharing :: Gnutella
Topic :: Communications :: File Sharing :: Napster
Topic :: Communications :: Ham Radio
Topic :: Communications :: Internet Phone
Topic :: Communications :: Telephony
Topic :: Communications :: Usenet News
Topic :: Database :: Database Engines/Servers
Topic :: Database :: Front-Ends
Topic :: Desktop Environment :: File Managers
Topic :: Desktop Environment :: GNUstep
Topic :: Desktop Environment :: Gnome
Topic :: Desktop Environment :: K Desktop Environment (KDE)
Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes
Topic :: Desktop Environment :: PicoGUI
Topic :: Desktop Environment :: PicoGUI :: Applications
Topic :: Desktop Environment :: PicoGUI :: Themes
Topic :: Desktop Environment :: Screen Savers
Topic :: Documentation :: Sphinx
Topic :: Education
Topic :: Education :: Computer Aided Instruction (CAI)
Topic :: Education :: Testing
Topic :: Games/Entertainment
Topic :: Games/Entertainment :: Arcade
Topic :: Games/Entertainment :: Board Games
Topic :: Games/Entertainment :: First Person Shooters
Topic :: Games/Entertainment :: Fortune Cookies
Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)
Topic :: Games/Entertainment :: Puzzle Games
Topic :: Games/Entertainment :: Real Time Strategy
Topic :: Games/Entertainment :: Role-Playing
Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games
Topic :: Games/Entertainment :: Simulation
Topic :: Games/Entertainment :: Turn Based Strategy
Topic :: Home Automation
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: Finger
Topic :: Internet :: Log Analysis
Topic :: Internet :: Name Service (DNS)
Topic :: Internet :: Proxy Servers
Topic :: Internet :: WAP
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki
Topic :: Internet :: WWW/HTTP :: HTTP Servers
Topic :: Internet :: WWW/HTTP :: Indexing/Search
Topic :: Internet :: WWW/HTTP :: Session
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Internet :: WWW/HTTP :: WSGI
Topic :: Internet :: WWW/HTTP :: WSGI :: Application
Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware
Topic :: Internet :: WWW/HTTP :: WSGI :: Server
Topic :: Internet :: XMPP
Topic :: Internet :: Z39.50
Topic :: Multimedia
Topic :: Multimedia :: Graphics
Topic :: Multimedia :: Graphics :: 3D Modeling
Topic :: Multimedia :: Graphics :: 3D Rendering
Topic :: Multimedia :: Graphics :: Capture
Topic :: Multimedia :: Graphics :: Capture :: Digital Camera
Topic :: Multimedia :: Graphics :: Capture :: Scanners
Topic :: Multimedia :: Graphics :: Capture :: Screen Capture
Topic :: Multimedia :: Graphics :: Editors
Topic :: Multimedia :: Graphics :: Editors :: Raster-Based
Topic :: Multimedia :: Graphics :: Editors :: Vector-Based
Topic :: Multimedia :: Graphics :: Graphics Conversion
Topic :: Multimedia :: Graphics :: Presentation
Topic :: Multimedia :: Graphics :: Viewers
Topic :: Multimedia :: Sound/Audio
Topic :: Multimedia :: Sound/Audio :: Analysis
Topic :: Multimedia :: Sound/Audio :: CD Audio
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing
Topic :: Multimedia :: Sound/Audio :: Capture/Recording
Topic :: Multimedia :: Sound/Audio :: Conversion
Topic :: Multimedia :: Sound/Audio :: Editors
Topic :: Multimedia :: Sound/Audio :: MIDI
Topic :: Multimedia :: Sound/Audio :: Mixers
Topic :: Multimedia :: Sound/Audio :: Players
Topic :: Multimedia :: Sound/Audio :: Players :: MP3
Topic :: Multimedia :: Sound/Audio :: Sound Synthesis
Topic :: Multimedia :: Sound/Audio :: Speech
Topic :: Multimedia :: Video
Topic :: Multimedia :: Video :: Capture
Topic :: Multimedia :: Video :: Conversion
Topic :: Multimedia :: Video :: Display
Topic :: Multimedia :: Video :: Non-Linear Editor
Topic :: Office/Business
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Accounting
Topic :: Office/Business :: Financial :: Investment
Topic :: Office/Business :: Financial :: Point-Of-Sale
Topic :: Office/Business :: Financial :: Spreadsheet
Topic :: Office/Business :: Groupware
Topic :: Office/Business :: News/Diary
Topic :: Office/Business :: Office Suites
Topic :: Office/Business :: Scheduling
Topic :: Other/Nonlisted Topic
Topic :: Printing
Topic :: Religion
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Artificial Intelligence
Topic :: Scientific/Engineering :: Artificial Life
Topic :: Scientific/Engineering :: Astronomy
Topic :: Scientific/Engineering :: Atmospheric Science
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)
Topic :: Scientific/Engineering :: GIS
Topic :: Scientific/Engineering :: Human Machine Interfaces
Topic :: Scientific/Engineering :: Hydrology
Topic :: Scientific/Engineering :: Image Processing
Topic :: Scientific/Engineering :: Image Recognition
Topic :: Scientific/Engineering :: Information Analysis
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Medical Science Apps.
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Visualization
Topic :: Security
Topic :: Security :: Cryptography
Topic :: Sociology
Topic :: Sociology :: Genealogy
Topic :: Sociology :: History
Topic :: Software Development
Topic :: Software Development :: Assemblers
Topic :: Software Development :: Bug Tracking
Topic :: Software Development :: Build Tools
Topic :: Software Development :: Code Generators
Topic :: Software Development :: Compilers
Topic :: Software Development :: Debuggers
Topic :: Software Development :: Disassemblers
Topic :: Software Development :: Documentation
Topic :: Software Development :: Embedded Systems
Topic :: Software Development :: Internationalization
Topic :: Software Development :: Interpreters
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Application Frameworks
Topic :: Software Development :: Libraries :: Java Libraries
Topic :: Software Development :: Libraries :: PHP Classes
Topic :: Software Development :: Libraries :: Perl Modules
Topic :: Software Development :: Libraries :: Pike Modules
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Libraries :: Ruby Modules
Topic :: Software Development :: Libraries :: Tcl Extensions
Topic :: Software Development :: Libraries :: pygame
Topic :: Software Development :: Localization
Topic :: Software Development :: Object Brokering
Topic :: Software Development :: Object Brokering :: CORBA
Topic :: Software Development :: Pre-processors
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Acceptance
Topic :: Software Development :: Testing :: BDD
Topic :: Software Development :: Testing :: Mocking
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: Software Development :: Testing :: Unit
Topic :: Software Development :: User Interfaces
Topic :: Software Development :: Version Control
Topic :: Software Development :: Version Control :: Bazaar
Topic :: Software Development :: Version Control :: CVS
Topic :: Software Development :: Version Control :: Git
Topic :: Software Development :: Version Control :: Mercurial
Topic :: Software Development :: Version Control :: RCS
Topic :: Software Development :: Version Control :: SCCS
Topic :: Software Development :: Widget Sets
Topic :: System
Topic :: System :: Archiving
Topic :: System :: Archiving :: Backup
Topic :: System :: Archiving :: Compression
Topic :: System :: Archiving :: Mirroring
Topic :: System :: Archiving :: Packaging
Topic :: System :: Benchmark
Topic :: System :: Boot
Topic :: System :: Boot :: Init
Topic :: System :: Clustering
Topic :: System :: Console Fonts
Topic :: System :: Distributed Computing
Topic :: System :: Emulators
Topic :: System :: Filesystems
Topic :: System :: Hardware
Topic :: System :: Hardware :: Hardware Drivers
Topic :: System :: Hardware :: Mainframes
Topic :: System :: Hardware :: Symmetric Multi-processing
Topic :: System :: Installation/Setup
Topic :: System :: Logging
Topic :: System :: Monitoring
Topic :: System :: Networking
Topic :: System :: Networking :: Firewalls
Topic :: System :: Networking :: Monitoring
Topic :: System :: Networking :: Monitoring :: Hardware Watchdog
Topic :: System :: Networking :: Time Synchronization
Topic :: System :: Operating System
Topic :: System :: Operating System Kernels
Topic :: System :: Operating System Kernels :: BSD
Topic :: System :: Operating System Kernels :: GNU Hurd
Topic :: System :: Operating System Kernels :: Linux
Topic :: System :: Power (UPS)
Topic :: System :: Recovery Tools
Topic :: System :: Shells
Topic :: System :: Software Distribution
Topic :: System :: System Shells
Topic :: System :: Systems Administration
Topic :: System :: Systems Administration :: Authentication/Directory
Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP
Topic :: System :: Systems Administration :: Authentication/Directory :: NIS
Topic :: Terminals
Topic :: Terminals :: Serial
Topic :: Terminals :: Telnet
Topic :: Terminals :: Terminal Emulators/X Terminals
Topic :: Text Editors
Topic :: Text Editors :: Emacs
Topic :: Text Editors :: Integrated Development Environments (IDE)
Topic :: Text Editors :: Text Processing
Topic :: Text Editors :: Word Processors
Topic :: Text Processing
Topic :: Text Processing :: Filters
Topic :: Text Processing :: Fonts
Topic :: Text Processing :: General
Topic :: Text Processing :: Indexing
Topic :: Text Processing :: Linguistic
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: LaTeX
Topic :: Text Processing :: Markup :: Markdown
Topic :: Text Processing :: Markup :: SGML
Topic :: Text Processing :: Markup :: VRML
Topic :: Text Processing :: Markup :: XML
Topic :: Text Processing :: Markup :: reStructuredText
Topic :: Utilities""".split("\n")

try:
    from trove_classifiers import classifiers
    topic_trove = [line for line in classifiers if re.match("Topic ::", line)]
except:
    pass
