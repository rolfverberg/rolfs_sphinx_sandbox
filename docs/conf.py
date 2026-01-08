# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute
sys.path.insert(0, os.path.abspath('../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rolfs_sphinx_sandbox'
copyright = f'{date.today().year}, Rolf Verberg'
author = 'Rolf Verberg'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages',
    'myst_parser',
]
#autodoc_mock_imports = ['any_package_like_numpy_or_list_of_packages']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]
source_suffix = ['.rst', '.md']
templates_path = ['_templates']

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# Use the myst_enable_extensions option to allow inline ($...$) and display
# ($$...$$) math syntax in Markdown files
myst_enable_extensions = [
    "dollarmath",
    "amsmath", # Optional: for advanced LaTeX environments like 'align'
]
mathjax3_config = {
    'tex2jax': {
        'inlineMath': [ ["\\(","\\)"] ],
        'displayMath': [["\\[","\\]"] ],
    },
    "tex": {
        "inlineMath": [["\\(", "\\)"]],
        "displayMath": [["\\[", "\\]"]],
    }
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'python_docs_theme' # Python Documentation theme
html_theme = 'sphinx_rtd_theme' # Read the Docs theme
#html_theme = 'sphinxdoc'    # Sphinx ducumentation theme
html_static_path = ['_static']
html_static_path = []
html_show_copyright = False
html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ],
    'using/windows': [
        'windows-sidebar.html',
        'searchbox.html'
    ],
}

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

