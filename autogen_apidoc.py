import os
import re
import subprocess

re_ext       = re.compile('(/?__init__\.py|\.py)$')
re_separator = re.compile('/')
src_path     = 'passerine'
index_tmpl   = """
API Reference
#############

.. toctree::
    :maxdepth: 1
    :glob:

    *

"""
module_tmpl  = """
{module_path}
{underline}

.. note::

    This page is automatically generated. If you don't see anything, this means
    this sub-module is not meant to be used. If you really want to know what it
    is, please check out the source code at :file:`{relative_path}`.

.. automodule:: {module_path}
    :members:
"""

def traverse(path):
    for name in os.listdir(path):
        if '__init__' in name:
            continue

        relative_path = os.path.join(path, name)

        if os.path.isdir(relative_path):
            traverse(relative_path)

            continue

        module_path   = re_separator.sub('.', re_ext.sub('', relative_path))

        #print(name, relative_path, module_path)

        with open('docs/source/api/{}.rst'.format(module_path), 'w') as f:
            f.write(module_tmpl.format(
                module_path   = module_path,
                relative_path = relative_path,
                underline     = "#" * len(module_path)
            ))

if __name__ == '__main__':
    # Remove all files.
    subprocess.call('rm docs/source/api/*', shell=True)

    # Generate the index page.
    with open('docs/source/api/index.rst', 'w') as f:
        f.write(index_tmpl)

    # Recursively generate API pages for the library.
    traverse(src_path)