# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_satispaython',
 'django_satispaython.migrations',
 'django_satispaython.templatetags']

package_data = \
{'': ['*'], 'django_satispaython': ['templates/django_satispaython/*']}

install_requires = \
['django>=3,<4', 'satispaython']

setup_kwargs = {
    'name': 'django-satispaython',
    'version': '0.1.3',
    'description': 'A simple django app to manage Satispay payments following the Web-button flow.',
    'long_description': "# django-satispaython\n\nA simple django app to manage Satispay payments following the [Web-button flow](https://developers.satispay.com/docs/web-button-pay).\n\n## Requirements\n\n* python >= 3.6\n* django >= 3\n* [`satispaython`](https://github.com/otto-torino/satispaython) >= 0.2\n\n## Installation\n\nYou can install this package with pip: `pip install django-satispaython`.\n\n## Usage\n\n### Key generation and key-id\n\nIn order to use django-satispaython you need to generate a [RSA private key](https://developers.satispay.com/reference#genereate-rsa-keys) and then get a [key-id](https://developers.satispay.com/reference#keyid).\nDjango-satispaython is based on [satispaython](https://github.com/otto-torino/satispaython) so you can import it, [create a key](https://github.com/otto-torino/satispaython#key-generation) and [obtain a key-id](https://github.com/otto-torino/satispaython#obtain-a-key-id-using-a-token).\n\n### Configuration\n\nOnce you created a RSA key and got a key-id add django-satispaython to your INSTALLED_APPS:\n\n```python\nINSTALLED_APPS = (\n  #...\n  'django_satispaython.apps.DjangoSatispaythonConfig',\n  #...\n)\n```\n\nThen add the followings to you django settings:\n\n```python\nSATISPAYTHON_PRIVATE_KEY_PATH = '/path/to/my/key.pem'\nSATISPAYTHON_KEY_ID_PATH = '/path/to/my/key-id.txt'\nSATISPAYTHON_STAGING = True\n```\n\n* `SATISPAYTHON_PRIVATE_KEY_PATH`: the path of your PEM file containing the RSA private key used to get your key-id.\n* `SATISPAYTHON_KEY_ID_PATH`: the path of the file containing the key-id coupled with the private-key.\n* `SATISPAYTHON_STAGING`: if `True` django-satispaython will use the [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints.\n\n### Satispay API\n\nIn order to use the [Satispay API](https://developers.satispay.com/reference) import django-satispaython.api:\n\n```python\nfrom django_satispaython import api as satispay\n```\n\nThen you can:\n\n#### Create a payment\n\n```python\nsatispay.create_payment(amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None)\n```\n\nYou may use satispaython utility function [`format_datetime`](https://github.com/otto-torino/satispaython#create-a-payment) to get a correctly formatted `expiration_date` to supply to the request.\n\n#### Get payment details\n\n```python\nsatisapy.get_payment_details(payment_id)\n```\n\n## Templatetags\n\nIn order to render the Satispay button just load the tag and use it in the template:\n\n```\n{% load django_satispaython %}\n...\n{% satispay_button payment_id=<your_payment_id> %}\n```\n\nNote that the button will automatically point at the endpoint (production or sandbox) specified in the project [`settings`](https://github.com/otto-torino/django-satispaython#configuration).\n\n## Database and Admin\n\nDjango-satispaython comes with a SatispayPayment model which contains every info associated to a payment and automatically show it in the admin page.\n\n> :information_source: All the Satispay API functions return an instance of the SatispayPayment model *without* actually storing it.\n\nIf you want to store a newly created payment in the database or update an already existing one with the informations provided by the response, set the `update` parameter to `True`.\n\n```python\nsatispay.create_payment(amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, update=True)\nsatisapy.get_payment_details(payment_id, update=True)\n```\n\nIn this case an output similar to django's [`update_or_create`](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#update-or-create) will be returned.\n\n## TODOS\n\n* Signals\n* ImproperlyConfiguredException",
    'author': 'Daniele Pira',
    'author_email': 'daniele.pira@otto.to.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otto-torino/django-satispaython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
