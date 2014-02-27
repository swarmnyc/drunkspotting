
Configure service
=================
Create a file called config.py that contains:

    config = {
        'database_server': '127.0.0.1',
        'database': 'XXX',
        'database_user': 'XXX',
        'database_password': 'XXX',
        'server_port': 8200,
        'azure_account': 'XXX',
        'azure_key': 'XXX',
        'upload_url': 'http://uploads.drunkspotting.com/'
    }

API Overview
============

Templates are pictures that have not been drawn on.
Pictures have been drawn on. Other than that
they are the same from an API standpoint.

GET /templates/[id]
===================

Get a specific template. See /pictures/[id] for what it returns.

[DEPRECATE] Just use /pictures/[id]

GET /pictures/[id]
==================

Get a specific picture.

    dictionarary {
        'template_id': 123,  # or null if no template
        'is_template': true/false,
        'title': 'xxx',
        'description': 'xxx',
        'latitude': 11.11,
        'longitude': 11.11,
        'rating': 1-5,
        'rating_count': 123,
        'url': 'http:/xxx',
        'time_posted': 'xxx'
    }

GET /templates/latest/[n]
=========================

Get the last n templates. See /pictures/latest/[n] for what it returns.

GET /pictures/latest/[n]
=========================

Get the last n pictures. An array of dictionaries.

    dictionary {
        'id': xxx,
        'template_id': xxx (or null)
        'title': 'xxx',
        'latitude': 11.11,
        'longitude': 11.11,
        'description': 'xxx',
        'rating': 1-5,
        'rating_count': 123,
        'url': 'http:/xxx',
        'time_posted': 'xxx'
    }

GET /pictures/[id]/comments/latest/[n]
=======================================

Get the last n comments for a template. An array of dictionaries.
The id is for a picture (template or not).

    dictionary {
        'id': xxx,
        'nick': 'xxx',
        'title': 'xxx',
        'description': 'xxx',
        'up_votes': n,
        'down_votes': n',
        'time_posted': 'xxx'
    }

POST /upload_template
=====================

See /upload

[DEPRECATES] Use /upload

POST /upload_template
=====================

See /upload

[DEPRECATES] Use /upload

POST /upload
=====================

Upload a new image. Post the image data.
Form example is:

    <form method="POST" enctype="multipart/form-data" action="http://api.drunkspotting.com/upload_template">
     <input id="data" type="file" name="data" />
     <input type="submit"/>
    </form>

Full raw binary data can also be sent, in addition to multipart/form-data.

A dictionary is returned:

    dictionary {
        'url': 'xxx'
    }

POST /templates/
================

See POST /templates/

[DEPRECATES] Use POST /templates/ (setting the is_template key)

POST /pictures/
===============

Add a template. The URL may be blank.

Post data is:

    dictionary {
        "is_template": true/false,
        "title": "xxx",
        "latitude": 12.34,
        "longitude": 23.34,
        "description": "xxx",
        "url": "http://xxx"
    }

Returned data:

    dictionary {
        "id": xxx
    }

POST /pictures/[id]/comments
============================

Post a comment to a given picture.

Post data is:

    dictionary {
        "nick": "xxx",
        "title": "xxx",
        "description": "xxx"
    }

Returned data:

    dictionary {
        "id": xxx
    }
