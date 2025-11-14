# Configuration file for the Sphinx documentation builder.
# docs/source/conf.py

import os
import sys
import datetime

# Add the project to the Python path
sys.path.insert(0, os.path.abspath('..'))  

# Project information
project = 'Simulateur de Trafic Routier Intelligent'
copyright = '2025, Aya Zid'
author = 'Aya Zid'
release = '1'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
    'autoapi.extension', 

]

# AutoAPI configuration
autoapi_type = 'python'
autoapi_dirs = ['../..']
autoapi_add_toctree_entry = True
autoapi_root = 'api'
autoapi_keep_files = False

# Napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True

# HTML theme
html_theme = 'sphinx_rtd_theme'

# Theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'titles_only': False,
    'display_version': True,
}

# Static files
html_static_path = ['_static']

# Master document
master_doc = 'index'

# Language
language = 'fr'

# Enable TODOs
todo_include_todos = True

# AutoAPI options
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]