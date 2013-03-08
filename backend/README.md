
Configure service
=================
Create a file called config.py that contains:

config = {
    'database': 'XXX',
    'database_user': 'XXX',
    'database_password': 'XXX',
    'server_port': 8200,
    'azure_account': 'XXX',
    'azure_key': 'XXX',
    'upload_url': 'http://drunkspotting.blob.core.windows.net/'
}

API Overview
============

Templates are pictures that hae not been drawn on.
Pictures have been drawn on. Other than that
they are pretty much the same from an API standpoint.

GET /templates/<id>
===================

Get a specific template.

dictionary {
    'title': 'xxx',
    'latitude': 11.11,
    'longitude': 11.11,
    'description': 'xxx',
    'rating': 1-5,
    'rating_count': 123,
    'url': 'http:/xxx',
    'time_posted': 'xxx'
}

GET /templates/latest/<n>
=========================

Get the last n templates. An array of dictionaries.

dictionary {
    'id': xxx
    'title': 'xxx',
    'latitude': 11.11,
    'longitude': 11.11,
    'description': 'xxx',
    'rating': 1-5,
    'rating_count': 123,
    'url': 'http:/xxx',
    'time_posted': 'xxx'
}

GET /pictures/<id>
==================

Get a specific picture.

dictionary {
    template_id': xxx
    'title': 'xxx',
    'latitude': 11.11,
    'longitude': 11.11,
    'description': 'xxx',
    'rating': 1-5,
    'rating_count': 123,
    'url': 'http:/xxx',
    'time_posted': 'xxx'
}

Get a specific picture.

GET /templates/latest/<n>
=========================

Get the last n pictures. An array of dictionaries.

dictionary {
    'id': xxx,
    'template_id': xxx,
    'title': 'xxx',
    'latitude': 11.11,
    'longitude': 11.11,
    'description': 'xxx',
    'rating': 1-5,
    'rating_count': 123,
    'url': 'http:/xxx',
    'time_posted': 'xxx'
}

GET /templates/<id>/comments/latest/<n>
=======================================

Get the last n comments for a template. An array of dictionaries.
The id is for a template.

dictionary {
    'id': xxx,
    'nic': 'xxx',
    'title': 'xxx',
    'description': 'xxx',
    'up_votes': n,
    'down_votes': n',
    'time_posted': 'xxx'
}

GET /pictures/<id>/comments/latest/<n>
======================================

Get the last n comments for a picture. An array of dictionaries.
The id is for a picture.

dictionary {
    'id': xxx,
    'nic': 'xxx',
    'title': 'xxx',
    'description': 'xxx',
    'up_votes': n,
    'down_votes': n',
    'time_posted': 'xxx'
}

POST /upload_template
=====================

Upload a new template image.

POST /upload_pictures
=====================

Upload a new picture.

POST /templates/
================

Add a template. The URL may be blank.

Post data is:

dictionary {
    "title": "xxx",
    "latitude": 12.34,
    "longitude": 23.34,
    "description": "xxx",
    "url": "http://xxx"
}

Returned data:

dictionary {
    "id": xxx,
    "token": "yyy"
}

ID is the id of the template. Token
can be used to update the template
withing a short time.

POST /pictures/
===============

Add a template. The URL may be blank.

Post data is:

dictionary {
    "template_id": xxx
    "title": "xxx",
    "latitude": 12.34,
    "longitude": 23.34,
    "description": "xxx",
    "url": "http://xxx"
}

Returned data:

dictionary {
    "id": xxx,
    "token": "yyy"
}

POST /templates/<id>/comments
=============================

Post a comment to a given template.

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

POST /pictures/<id>/comments
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



