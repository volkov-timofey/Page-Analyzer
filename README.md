### Hexlet tests and linter status:
[![Actions Status](https://github.com/volkov-timofey/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/volkov-timofey/python-project-83/actions)
[![Python CI](https://github.com/volkov-timofey/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/volkov-timofey/python-project-83/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/4939aaceb73bd854568b/maintainability)](https://codeclimate.com/github/volkov-timofey/python-project-83/maintainability)


### Information
Page Analyzer is a site that analyzes specified pages for SEO suitability.

### Demo application
[https://page-analyzer-c72h.onrender.com/](https://page-analyzer-c72h.onrender.com/)

### Install

#### Prepare the database.

##### Before installing the application, prepare your environment variables:
* DATABASE_URL
    > For example: DATABASE_URL=postgresql://user:password@localhost:5432/mydb
* SECRET_KEY

#### Clone the repository and run application:
```bash
$ git clone https://github.com/volkov-timofey/Page-Analyzer.git
$ cd python-project-83
$ make build
$ make start
```
