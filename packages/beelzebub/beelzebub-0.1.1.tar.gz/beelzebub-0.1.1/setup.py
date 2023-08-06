# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beelzebub', 'beelzebub.base']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'logging-config>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'beelzebub',
    'version': '0.1.1',
    'description': 'Lightweight framework for transforming input to output',
    'long_description': "# beelzebub\n\nBeelzebub is a lightweight framework to transform input to output.  The base classes aren't meant to be used directly, rather they establish the interfaces of the framework, and provide a basis with which to derive classes for defining a particular transformation workflow.\n\nA workflow consists of a reader class, a writer class, and a processor class.  The workflow class instantiates one of each of these classes, and then executes the workflow of reading input from a given *source* via the reader class, writing output to a given *sink* via the writer class, and the processor class calls the reader and passes the read input to the writer.\n\nBoth the reader and writer classes are based on a common context manager class.  In particular, the `open()` method can read/write to one of a set of supported *iostream* types.  The *iotype* should be one of `['file','url','str']` and defaults to `str`.\n\nThe workflow class can optionally setup logging for the workflow (based on the existence of a `logger` section in the optional configuration dict), and then calls the `run()` method, passing the source and sink.\n\nAs mentioned, an optional configuration dict can be passed when instantiating the workflow object.  As a particular workflow will have specific reader, writer and processor classes, the configuration items for each of these components is arbitrary, suited to the particular workflow.  However, the framework will look for a toplevel key called `reader` to pass to the reader class, `writer` to pass to the writer class, and `processor` to pass to the processor class.  In addition, if a `logger` key exists, then this will be used to configure logging, via a call to `logging.config.dictConfig(logging_conf)`.\n\nOne of the main uses of the configuration is to specify the iotype for the reader and writer.  For example, if the input is read from a file, but the output is to be written to a string, then at least a `reader` configuration is required, as `file` is not the default iotype for the reader:\n\n```python\nconf = {'reader': {'iotype': 'file'}, 'writer': {'iotype': 'str'}}\nin_file = sys.argv[1]\nout_file = None\n\nx = BaseWorkflow(conf=conf)\nx.run(in_file, out_file)\nprint(x.writer.output)\n```\n\nNote that if the output is to be written to a string, then the sink argument (here, `out_file`) to `run()` is redundant, and can be set to `None`.  In this case, access the output string via the workflow's writer's `output` attribute.\n\n",
    'author': 'Paul Breen',
    'author_email': 'paul.breen6@btinternet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paul-breen/beelzebub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
