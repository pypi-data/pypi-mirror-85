# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quickbase_client',
 'quickbase_client.client',
 'quickbase_client.orm',
 'quickbase_client.query',
 'quickbase_client.tools',
 'quickbase_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'requests>=2.24.0,<3.0.0', 'stringcase>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['qbc = quickbase_client.tools.qbc:main']}

setup_kwargs = {
    'name': 'quickbase-client',
    'version': '0.1.0',
    'description': 'A QuickBase Python API Client Generator',
    'long_description': '#####################\nQuickBase-Client\n#####################\n\nA High-Level QuickBase Python API Client & Model Generator\n\n\n.. image:: https://gitlab.com/tkutcher/quickbase-client/badges/dev/pipeline.svg\n    :target: https://gitlab.com/tkutcher/quickbase-client/-/commits/dev\n    :alt: Pipeline Status\n\n.. image:: https://gitlab.com/tkutcher/quickbase-client/badges/dev/coverage.svg\n    :target: https://gitlab.com/tkutcher/quickbase-client/-/commits/dev\n    :alt: Coverage Report\n\n.. image:: https://readthedocs.org/projects/quickbase-client/badge/?version=latest\n    :target: https://quickbase-client.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://badge.fury.io/py/quickbase-client.svg\n    :target: https://badge.fury.io/py/quickbase-client\n    :alt: PyPI\n\n|\n\n\n*QuickBase-Client is a library for interacting with QuickBase applications through their\nRESTful JSON API (https://developer.quickbase.com/). It has features to generate model classes\nfor tables in your QuickBase app, and provides high level classes to interface between Python\nobjects and the QuickBase tables.*\n\n|\n\nQuick Start\n============\n\n\nInstallation\n____________\n\nInstallation can be done through pip:\n\n.. code-block:: bash\n\n    pip install quickbase-client\n\nThis will install both the library ``quickbase_client``, and a command line tool ``qbc`` for\nrunning some handy scripts.\n\n\nGenerating your Models\n----------------------\n\nTo interact and authenticate with your QuickBase applications you need a User Token. You can read\nthe QuickBase documentation `here <https://developer.quickbase.com/auth>`_ on how to create one.\nIt is recommended to set an environment variable ``QB_USER_TOKEN`` with this value:\n\n.. code-block:: bash\n\n    export QB_USER_TOKEN=mytokenfromquickbase;\n\n\nNext, say you have a hypothetical QuickBase Application named MyApp at\n``https://foo.quickbase.com/db/abcdef`` that has tables for tracking things\nagainst a repository like Issues & Pipelines.\n\n\n.. image:: /images/example_table.png\n    :width: 500\n    :alt: Example Table\n\n|\n\nRunning the following:\n\n.. code-block:: bash\n\n    qbc run model-generate -a https://foo.quickbase.com/db/abcdef\n\nWould generate a directory structure like\n\n::\n\n    models\n    ├── __init__.py\n    └── my_app\n        ├── __init__.py\n     \xa0\xa0 ├── app.py\n    \xa0\xa0  ├── github_issue.py\n    \xa0\xa0  └── gitlab_pipeline.py\n\nAnd classes like ``GitHubIssue`` where you can interact with the data model through a Python object.\n\n\nWriting Records to QuickBase\n----------------------------\n\nClasses like ``GitHubIssue`` that subclass ``QuickBaseTable`` also get a factory class-method\n``client(user_tok)`` which creates an instance of the higher-level ``QuickBaseTableClient`` to\nmake API requests for things related to that table:\n\n.. code-block:: python\n\n    client = GitHubIssue.client(user_tok=os.environ[\'QB_USER_TOKEN\'])\n    new_issue = GitHubIssue(\n        title=\'Something broke\',   # you get friendly-kwargs for fields without worrying about ID\'s\n        description=\'Please fix!\',\n        date_opened=date.today()   # things like Python date objects will be serialized\n    )\n    response = client.add_record(new_issue)\n    print(response.json())  # all methods (except for query) return the requests Response object\n\n\nQuerying Records from QuickBase\n-------------------------------\n\nYou can also use the client object to send queries to the QuickBase API through the ``query``\nmethod. This method will serialize the data back in to a Python object. The `query` method on the\ntable class takes a ``QuickBaseQuery`` object which is high level wrapper around the parameters\nneeded to make a query.\n\nNotably, the ``where`` parameter for specifying the query string. There is one (and in the future\nthere will be more) implementation of this which allows you to build query-strings through\nhigher-level python functions.\n\nYou can use the methods exposed in the ``quickbase_client.query`` module like so:\n\n.. code-block:: python\n\n    # convention to append an underscore to these methods to avoid clashing\n    # with any python keywords\n    from quickbase_client.query import on_or_before_\n    from quickbase_client.query import eq_\n    from quickbase_client.query import and_\n\n    schema = GitHubIssue.schema\n    q = and_(\n        eq_(schema.date_opened, schema.date_created),\n        on_or_before_(schema.date_closed, date(2020, 11, 16))\n    )\n    print(q.where)  # ({\'9\'.EX.\'_FID_1\'}AND{\'10\'.OBF.\'11-16-2020\'})\n    recs = client.query(q)  # recs will be GitHubIssue objects unless passing raw=True\n    print([str(r) for r in recs])  # [\'<GitHubIssue title="Made And Closed Today" id="10000">\']\n\n\n\nControlling Lower-Level API Calls\n---------------------------------\n\nLastly, say you want to deal with just posting the specific json/data QuickBase is looking for.\nThe ``QuickBaseTableClient`` object wraps the lower-level ``QuickBaseApiClient`` object which has\nmethods for just sending the actual data (with an even lower-level utility\n``QuickBaseRequestFactory`` you could also use). These classes manage hanging on to the user token,\nand the realm hostname, etc. for each request that is made.\n\nFor example, note the signature of ``query`` in ``QuickBaseApiClient``:\n\n.. code-block:: python\n\n    def query(self, table_id, fields_to_select=None, where_str=None,\n              sort_by=None, group_by=None, options=None):\n\n\nYou can get to this class by going through the table client: ``api = client.api``, or from\ninstantiating it directly ``api = QuickBaseApiClient(my_user_token, my_realm)``\n\nWith this, we could make the exact same request as before:\n\n.. code-block:: python\n\n    api = QuickBaseApiClient(user_token=\'my_token\', realm_hostname=\'foo.quickbase.com\')\n    response = api.query(\n        table_id=\'abcdef\',\n        where_str="({\'9\'.EX.\'_FID_1\'}AND{\'10\'.OBF.\'11-16-2020\'})")\n    data = response.json()\n\n\n.. exclusion-marker-do-not-remove\n\nMore Resources\n==============\n- `examples </examples>`_ directory.\n\n\nContributing\n============\n- Coming soon\n',
    'author': 'Tim Kutcher',
    'author_email': 'tim@tkutcher.com',
    'maintainer': 'Tim Kutcher',
    'maintainer_email': 'tim@tkutcher.com',
    'url': 'https://github.com/tkutcher/quickbase-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
