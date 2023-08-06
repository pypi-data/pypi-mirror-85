ddb (for Docker Devbox)
===

[![PyPI](https://img.shields.io/pypi/v/docker-devbox-ddb)](https://pypi.org/project/docker-devbox-ddb/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docker-devbox-ddb)](https://pypi.org/project/docker-devbox-ddb/)
[![PyPI - License](https://img.shields.io/pypi/l/docker-devbox-ddb)](https://github.com/gfi-centre-ouest/docker-devbox-ddb/blob/develop/LICENSE)
[![Build Status](https://img.shields.io/travis/gfi-centre-ouest/docker-devbox-ddb.svg)](https://travis-ci.org/gfi-centre-ouest/docker-devbox-ddb)
[![Code coverage](https://img.shields.io/coveralls/github/gfi-centre-ouest/docker-devbox-ddb)](https://coveralls.io/github/gfi-centre-ouest/docker-devbox-ddb)

**[Erase environment differences, make developers happy !](https://gfi-centre-ouest.github.io/docker-devbox-ddb)**

**ddb** automates application configuration so differences between development, staging and production environment can 
be erased. It provides features to generate, activate and adjust **configuration files** based on a **single overridable 
and extendable configuration**, while **enhancing the developer experience** and **reducing manual operations**.

Primarly designed for [docker-compose](https://docs.docker.com/compose/) and [docker-devbox](https://github.com/gfi-centre-ouest/docker-devbox), 
this tool makes the developer **forget about the docker hard stuff** by providing commands right into it's PATH, so it's 
experience **looks like everything is native** and locally installed.

Thanks to a pluggable, event based and easy to extend architecture, it can bring **powerful configuration automation to 
any technical context**.

Install
-------

!!! warning "ddb should most often be installed by [docker-devbox](https://github.com/gfi-centre-ouest/docker-devbox-ddb)"
    You should better install the whole [docker-devbox](https://github.com/gfi-centre-ouest/docker-devbox-ddb) toolkit 
    to enjoy the experience.
    
    [docker-devbox](https://github.com/gfi-centre-ouest/docker-devbox-ddb) automatically installs **ddb** as a 
    dependency, along some **helper docker containers**.
    
    Only **advanced users** should install **ddb** on their own. If you are not sure what to do, do not install **ddb** 
    on your own, but follow [docker-devbox](https://github.com/gfi-centre-ouest/docker-devbox-ddb) installation docs.
    
**ddb** is supported on **Linux**, **Windows** and **MacOS**. 

You can **[download binary releases on github](https://github.com/gfi-centre-ouest/docker-devbox-ddb/releases)**, or 
install on Python 3.5+ with pip.

```
pip install docker-devbox-ddb
```
