# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_storages',
 'dynamic_storages.fields',
 'dynamic_storages.migrations',
 'dynamic_storages.models',
 'dynamic_storages.tasks',
 'dynamic_storages.tests',
 'dynamic_storages.tests.fields',
 'dynamic_storages.tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.0,<9.0.0',
 'apache-libcloud>=3.2.0,<4.0.0',
 'azure-storage-blob>=1.3.1,<12.0.0',
 'boto3>=1.16.8,<2.0.0',
 'django-appconf>=1.0.4,<2.0.0',
 'django-fernet-fields>=0.6,<0.7',
 'django-storages[dropbox,libcloud,boto3,google,sftp,azure]>=1.10.1,<2.0.0',
 'django>=3.1.0,<4.0.0',
 'dropbox>=10.8.0,<11.0.0',
 'google-cloud-storage>=1.32.0,<2.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'paramiko>=2.7.2,<3.0.0',
 'six>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'django-dynamic-storages',
    'version': '0.4.1',
    'description': 'A collection of file fields and associated components to allow for dynamic configuration of storage properties for file-based fields within Django models.',
    'long_description': '# Django Dynamic Storages\n\nI\'ll fill this in with more detail later, but the basic reasoning for this project is that I needed something I could use to extend the already excellent [django-storages](https://github.com/jschneier/django-storages) project such that the storage field on any given `FileField` was a callable I could source a model instance value from. I\'ve also included an abstract class for holding a configuration that stores (securely via [django-fernet-fields](https://github.com/orcasgit/django-fernet-fields)) the access configuration for a given storage backend as well.  \n\n## Goals\n\nI wanted a way to:\n\n* dynamically/at runtime, assign a `django-storages` backend to a given `FileField` in a model\n* dynamically/at runtime, manage the encryption/decryption of the contents of the aforementioned `FileField`\n* Ideally, I\'d like to be able to achieve this following idiomatic patterns from `django-storages` in terms of using callable kwargs to achieve this so that the consumer of these components had as much control over details as possible with the least amount of overhead.\n    * I took the [`upload_to`](https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.FileField.upload_to) implementation as inspiration for how to implement the above.\n\n## Components\n\n### Fields\n\n#### `dynamic_storages.fields.dynamic_storage`\n\n`DynamicStorageFileField` and `DynamicStorageImageField` are extensions each of the built-in Django [`FileField`](https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield) and [`ImageField`](https://docs.djangoproject.com/en/3.1/ref/models/fields/#integerfield) which utilizes the storage backends provided by [django-storages](https://django-storages.readthedocs.io/en/latest/). Rather than setting the `storage` kwarg at the field level, we\'re using a kwarg we named `storage_instance_callable` to manage the callable function workflow for determining the backend to use. This is, primarily, due to Django 3.0 allowing a callable to be passed in for the `storage` kwarg, however it does not pass the callable function any context - we simply sidestep that issue by using a different kwarg and then use that to set the storage value.\n\n\nFpr the sake of providing an example, the following is a real-world usage of this process using a callable function which takes the model instance in as an argument. It identifies if a \'team\' is attached to the instance and then finds the `TeamStorageTarget` (a separate model derived from `dynamic_storages.models.AbstractStorageTarget`)\n\n```python\ndef get_storage(instance):\n    if instance and getattr(instance, "team", None):\n        tst = TeamStorageTarget.for_team(instance.team)\n        if tst:\n            return tst.storage_backend\n    return default_storage\n```\n\n#### `dynamic_storages.fields.encrypted_content`\n\n`EncryptedFileField` and `EncryptedImageField` are extensions each of `DynamicStorageFileField` and `DynamicStorageImageField` with the main difference being that these new field definitions encapsulate the process of encrypting and decrypting content for their files at runtime. Two callables are needed to do this, both of which will receive the `instance` object when called:\n\n* `fernet` - the callable assigned to this should return a [`cryptography.fernet.Fernet`](https://cryptography.io/en/latest/fernet.html?highlight=fernet#cryptography.fernet.Fernet) or [`cryptography.fernet.MultiFernet\'](https://cryptography.io/en/latest/fernet.html?highlight=fernet#cryptography.fernet.Fernet) for the handling of encryption operations\n\n\n* `get_url` - the callable assigned to this should return a URL which is configured/designed to decrypt the content and serve it to the end user as appropriate (i.e. security is baked into your views, not into this field directly). An example of what a view might look like for this is located in [\'dynamic_storages/views.py\'](dynamic_storages/views.py).\n\nIn a real-world application, your callable for `get_url` might take multiple values from the instance the file belongs to and construct a url to return:\n\n```python\ndef file_content_url(instance):\n    return reverse_lazy("api:team-files-contents", args=[instance.file.team.slug, instance.team.id, instance.team.file.name.split(".")[-1]])\n```\n\nThe view that gets exposed for this `get_url` might be a custom action within a Django Rest Framework Viewset such as:\n\n```python\nclass FileViewSet(viewsets.ModelViewSet):\n    """other implementation details not included..."""\n\n    @action(detail=True, methods=["GET"], name="Get File Contents", url_path="contents.<str:file_ext>")\n    def contents(self, request, **kwargs):\n        user = request.user\n        try:\n            if request.user.is_authenticated():\n                team = get_object_or_404(Team, slug=kwargs.get("parent_lookup_team__slug"))\n                file_ext = self.kwargs["file_ext"]\n                if user_can_access_team(user, team):\n                    f = get_object_or_404(File, team=team, pk=kwargs["pk"])\n                    content = f.file.get_decrypted().read()\n                    return HttpResponse(\n                        content,\n                        content_type=magic.Magic(mime=True).from_buffer(content),\n                    )\n                else:\n                    log.warn("User {} is not allowed to access resources for team {}".format(user.username, team.name))\n            else:\n                log.warn("User is not authenticated for request to file with {}".format(self.kwargs))\n        except Exception as ex:\n            log.warn("Failed to get property for request: {}".format(ex))\n        raise Http404\n```\n\n#### `dynamic_storages.fields.encrypted_json`\n\nThe `EncryptedJSONField` is meant to be useful in handling the storage of things like storage credentials within a database. It was useful in our testing and we\'ve found that even though it follows an older pattern in the Django community around JSONFields (given that Django 3 has them built in now), this setup serves well for credential storage.  It leverages the [`django-fernet-fields`](https://github.com/orcasgit/django-fernet-fields) [`EncryptedTextField`](https://github.com/orcasgit/django-fernet-fields/blob/master/fernet_fields/fields.py#L109) as its storage medium and we\'re simply marshaling it back and forth from dictionary to string.  \n\n\n### Other Stuff\n\n###\n\n\n## To-Do\n\n* [ ] Update the `.models.AbstractStorageTarget` model to include credential checking\n* [ ] Create async task for handling credential checking periodically for `AbstractStorageTarget`-based storage\n* [ ] write more tests around the `default_storage` provider\n* [ ] look into further extending `django-storages` to handle google drive (since it already supports dropbox)\n\n## Revisions\n\n* `0.4.1` (Wed 18 Nov 2020 08:54:36 AM PST) - packaging updates to make pypi page point back to github and licence fix as this should be under an BSD-3 license due to upstream requirements, cleaned up logging in `AbstractStorageTarget` and setting up credential checking method for storage backends\n* `0.4.0` (Mon Nov 16 09:50:48 AM PST 2020) - readme updates, documentation fixes, more clarity/examples, added some todo\'s\n* `0.3.8` (Mon Nov 16 09:22:41 AM PST 2020) - docstring updates and some changes to the order of operations re: generating a download url for a file via callables\n* `0.3.7` (Mon Nov 16 09:05:32 AM PST 2020) - Fixing typo\n* `0.3.6` (Fri Nov 13 10:01:38 AM PST 2020) - consistency issues with get_url call again... mirroring process from the fernet setup\n* `0.3.5` (Thu Nov 12 03:53:03 PM PST 2020) - fixes to my `get_url` stuff - dumb misses\n* `0.3.4` (Thu Nov 12 11:42:21 AM PST 2020) - minor update to allow for a callable function to be passed in for an `EncryptedFileField` so that you can externally control the view/url that needs to be used to get the contents of this file.\n',
    'author': 'Patrick McClory',
    'author_email': 'patrick@mcclory.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcclory/django-dynamic-storages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
