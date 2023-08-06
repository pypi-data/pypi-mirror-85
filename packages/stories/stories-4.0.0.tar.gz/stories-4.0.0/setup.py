# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_stories',
 '_stories.contrib',
 '_stories.contrib.debug_toolbars',
 '_stories.contrib.debug_toolbars.django',
 '_stories.contrib.debug_toolbars.flask',
 '_stories.execute',
 'stories',
 'stories.contrib',
 'stories.contrib.debug_toolbars',
 'stories.contrib.sentry']

package_data = \
{'': ['*'],
 '_stories.contrib.debug_toolbars.django': ['templates/stories/debug_toolbar/*'],
 '_stories.contrib.debug_toolbars.flask': ['templates/stories/debug_toolbar/*']}

entry_points = \
{'pytest11': ['stories = stories.contrib.pytest']}

setup_kwargs = {
    'name': 'stories',
    'version': '4.0.0',
    'description': 'Define a user story in the business transaction DSL',
    'long_description': '# Stories\n\n[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)\n[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)\n[![pypi](https://img.shields.io/pypi/v/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)\n[![python](https://img.shields.io/pypi/pyversions/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)\n\nThe business transaction DSL.\n\n**[Documentation](https://proofit404.github.io/stories/) |\n[Source Code](https://github.com/proofit404/stories) |\n[Task Tracker](https://github.com/proofit404/stories/issues)**\n\n`stories` is a business transaction DSL. It provides a simple way to define a\ncomplex business transaction that includes processing over many steps and by\nmany different objects. It makes error handling a primary concern by taking a\n“[Railway Oriented Programming](http://fsharpforfunandprofit.com/rop/)” approach\nto capturing and returning errors from any step in the transaction.\n\n## Pros\n\n- Define a user story in the business transaction DSL.\n- Separate state, implementation and specification.\n- Clean flow in the source code.\n- Separate step implementation.\n- Each step knows nothing about a neighbor.\n- Easy reuse of code.\n- Allows to instrument code easily.\n- Explicit data contracts and relations in code.\n- Data store independent.\n- Catch errors when they occur.\n- Not when they propagate to exception.\n\n`stories` is based on the following ideas:\n\n- A business transaction is a series of operations where any can fail and stop\n  the processing.\n- A business transaction can describe its steps on an abstract level without\n  being coupled to any details about how individual operations work.\n- A business transaction doesn’t have any state.\n- Each operation shouldn’t accumulate state, instead it should receive an input\n  and return an output without causing any side-effects.\n- The only interface of an operation is `ctx`.\n- Each operation provides a meaningful piece of functionality and can be reused.\n- Errors in any operation should be easily caught and handled as part of the\n  normal application flow.\n\n## Example\n\n`stories` provide a simple way to define a complex business scenario that\ninclude many processing steps.\n\n```pycon\n\n>>> from stories import story, arguments, Success, Failure, Result\n>>> from app.repositories import load_category, load_profile, create_subscription\n\n>>> class Subscribe:\n...\n...     @story\n...     @arguments(\'category_id\', \'profile_id\')\n...     def buy(I):\n...\n...         I.find_category\n...         I.find_profile\n...         I.check_balance\n...         I.persist_subscription\n...         I.show_subscription\n...\n...     def find_category(self, ctx):\n...\n...         ctx.category = load_category(ctx.category_id)\n...         return Success()\n...\n...     def find_profile(self, ctx):\n...\n...         ctx.profile = load_profile(ctx.profile_id)\n...         return Success()\n...\n...     def check_balance(self, ctx):\n...\n...         if ctx.category.cost < ctx.profile.balance:\n...             return Success()\n...         else:\n...             return Failure()\n...\n...     def persist_subscription(self, ctx):\n...\n...         ctx.subscription = create_subscription(category=ctx.category, profile=ctx.profile)\n...         return Success()\n...\n...     def show_subscription(self, ctx):\n...\n...         return Result(ctx.subscription)\n\n>>> Subscribe().buy(category_id=1, profile_id=1)\nSubscription(primary_key=8)\n\n```\n\nThis code style allow you clearly separate actual business scenario from\nimplementation details.\n\n## Questions\n\nIf you have any questions, feel free to create an issue in our\n[Task Tracker](https://github.com/proofit404/stories/issues). We have the\n[question label](https://github.com/proofit404/stories/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)\nexactly for this purpose.\n\n## Enterprise support\n\nIf you have an issue with any version of the library, you can apply for a paid\nenterprise support contract. This will guarantee you that no breaking changes\nwill happen to you. No matter how old version you\'re using at the moment. All\nnecessary features and bug fixes will be backported in a way that serves your\nneeds.\n\nPlease contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you\'re\ninterested in it.\n\n## License\n\nStories library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐️ &mdash;</p>\n<p align="center"><i>The stories library is part of the SOLID python family.</i></p>\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/stories/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
