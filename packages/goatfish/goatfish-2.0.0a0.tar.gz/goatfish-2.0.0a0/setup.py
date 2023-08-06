# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goatfish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'goatfish',
    'version': '2.0.0a0',
    'description': 'A small, schemaless ORM that is backed by SQLite.',
    'long_description': 'Description\n===========\n\n[![Build Status](https://secure.travis-ci.org/stochastic-technologies/goatfish.png?branch=master)](http://travis-ci.org/stochastic-technologies/goatfish)\n[![Code Shelter](https://www.codeshelter.co/static/badges/badge-flat.svg)](https://www.codeshelter.co/)\n\n\n``goatfish`` is a small, schemaless ORM that is backed by SQLite.\n\nIt\'s also this:\n\n![A goatfish](https://upload.wikimedia.org/wikipedia/commons/d/da/Parupeneus_insularis.jpg)\n\nIts usage is very simple, just have your classes inherit from ``goatfish.Model``\nand and specify a connection, and the goatfish methods are available to you.\ngoatfish also supports querying for arbitrary properties in your models, as\nwell as indexing on arbitrary properties. It does not enforce a schema of any\nkind.\n\nIt appears that this method is identical to what FriendFeed used to implement\na schemaless layer over MySQL, which is pretty significant validation:\n\nhttp://backchannel.org/blog/friendfeed-schemaless-mysql\n\n\nUsage\n-----\n\nTo use ``goatfish``, all you need to do is create a class that inherits from\n``goatfish.Model``:\n\n    import goatfish\n    import sqlite3\n\n    db_connection = sqlite3.connect(":memory:")\n\n    class Test(goatfish.Model):\n        class Meta:\n            # This is so we know where to connect.\n            connection = db_connection\n            indexes = (\n                ("foo",),\n                ("foo", "bar"),\n            )\n\n    # Create the necessary tables. If they exist, do nothing.\n    Test.initialize()\n\n    foo = Test()\n    foo.foo = "hi"\n    foo.bar = "hello"\n    foo.save()\n\n    # Retrieve all elements.\n    >>> [test.bar for test in Test.all()]\n    [\'hello\']\n\n    # Count the number of elements.\n    >>> Test.count(foo="hi")\n    1\n\n    # Run a query with parameters (slow, loads every item from the DB to check it).\n    >>> [test.bar for test in Test.find(bar="hello")]\n    [\'hello\']\n\n    # This uses an index, so it\'s fast.\n    >>> [test.foo for test in Test.find(foo="hi"})]\n    [\'hi\']\n\n    # Run a query with a parameter that doesn\'t exist in the dataset.\n    >>> [test.bar for test in Test.find({bar="hello", baz="hi"})]\n    []\n\n    >>> Test.find_one(bar="hello").foo\n    "hi"\n\n    >>> print(Test.find_one(bar="doesn\'t exist"))\n    None\n\n    # Delete the element.\n    >>> foo.delete()\n\n    # Try to retrieve all elements again.\n    >>> [test.bar for test in Test.find()]\n    []\n\n\nIndexes\n-------\n\nWhat sets ``goatfish`` apart from other modules such as ``shelve``, ``zodb``,\netc is its ability to query random attributes, and make those queries faster\nby using SQLite indexes.\n\nThe way this is achieved is by creating an intermediate table for each index\nwe specify. The index tables consist of the uuid column, and one column for\nevery field in the index. This way, we can store the value itself in these\nindex tables and query them quickly, as the rows have SQLite indexes\nthemselves.\n\nThe find() method uses these indexes automatically, if they exist, to avoid\nsequential scans. It will automatically use the largest index that contains\nthe data we want to query on, so a query of ``{"foo": 3, "bar": 2}`` when only\n``foo`` is indexed will use the index on ``foo`` to return the data, and do a\nsequential scan to match ``bar``.\n\nRight now, new indexes are only populated with data on save(), so you might\nmiss rows when querying on indexes that are not ready yet. To populate indexes,\ngo through the objects in your model and perform a save() in each of them.\nConvenience functions to populate single indexes will be provided shortly.\n\n\nInstallation\n------------\n\nTo install ``goatfish`` you need:\n\n* Python 3.4 or later.\n\nYou have multiple options for installation:\n\n* With pip (preferred), do ``pip install goatfish``.\n* With setuptools, do ``easy_install goatfish``.\n* To install from source, download it from\n  https://github.com/stochastic-technologies/goatfish/ and do\n  ``python setup.py install``.\n\n\nLicense\n-------\n\n``goatfish`` is distributed under the BSD license.\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stochastic-technologies/goatfish/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
