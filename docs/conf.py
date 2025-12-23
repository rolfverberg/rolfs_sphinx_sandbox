# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rolfs_sphinx_sandbox'
copyright = '2025, Rolf Verberg'
author = 'Rolf Verberg'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
#    'sphinx.ext.autodoc',
    'autodoc2',
#    'sphinxarg.ext'
    'sphinx.ext.githubpages',
]
#autodoc_mock_imports = ['any_package_like_numpy_or_list_of_packages']
#autodoc2_packages = ['../src']
autodoc2_packages = ['../docs']
autodoc2_render_plugin = 'myst'
exclude_patterns = ['_build'] 
source_suffix = ['.rst', '.md']
templates_path = ['_templates']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
#html_theme = 'python_docs_theme' # Python Documentation theme
html_theme = 'sphinx_rtd_theme' # Read the Docs theme
#html_theme = 'sphinxdoc'    # Sphinx ducumentation theme
#html_static_path = ['_static']
html_static_path = []
html_show_copyright = False
#html_sidebars = {
#    '**': ['globaltoc.html',
#           'localtoc.html',
#           'relations.html',
#           'searchbox.html']
#}

