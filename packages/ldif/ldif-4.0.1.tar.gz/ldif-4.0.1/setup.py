# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ldif']
setup_kwargs = {
    'name': 'ldif',
    'version': '4.0.1',
    'description': 'generate and parse LDIF data (see RFC 2849).',
    'long_description': "ldif - generate and parse LDIF data (see `RFC 2849`_).\n======================================================\n\nThis is a fork of the ``ldif`` module from `python-ldap`_ with python3/unicode\nsupport.\n\nOne of its benefits is that it's a pure-python package (you don't depend\non the ``libldap2-dev`` (or similar) package that needs to be installed on\nyour laptop / test machine / production server.\n\nSee the first entry in CHANGES.rst for a more complete list of\ndifferences.\n\nThis package only support Python 3 (>= 3.6, actually).\n\n\nUsage\n-----\n\nParse LDIF from a file (or ``BytesIO``)::\n\n    from ldif import LDIFParser\n    from pprint import pprint\n\n    parser = LDIFParser(open('data.ldif', 'rb'))\n    for dn, entry in parser.parse():\n        print('got entry record: %s' % dn)\n        pprint(record)\n\n\nWrite LDIF to a file (or ``BytesIO``)::\n\n    from ldif import LDIFWriter\n\n    writer = LDIFWriter(open('data.ldif', 'wb'))\n    writer.unparse('mail=alice@example.com', {\n        'cn': ['Alice Alison'],\n        'mail': ['alice@example.com'],\n        'objectclass': ['top', 'person'],\n    })\n\nUnicode support\n---------------\n\nThe stream object that is passed to parser or writer must be an ascii byte\nstream.\n\nThe spec allows to include arbitrary data in base64 encoding or via URL. There\nis no way of knowing the encoding of this data. To handle this, there are two\nmodes:\n\nBy default, the ``LDIFParser`` will try to interpret all values as UTF-8 and\nleave only the ones that fail to decode as bytes. But you can also pass an\n``encoding`` of ``None`` to the constructor, in which case the parser will not\ntry to do any conversion and return bytes directly.\n\n\n.. _RFC 2849: https://tools.ietf.org/html/rfc2849\n.. _python-ldap: http://www.python-ldap.org/\n",
    'author': 'Abilian SAS',
    'author_email': 'dev@abilian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abilian/ldif',
    'py_modules': modules,
    'python_requires': '>3.6,<4',
}


setup(**setup_kwargs)
