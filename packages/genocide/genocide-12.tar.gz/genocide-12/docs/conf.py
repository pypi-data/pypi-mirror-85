# -*- coding: utf-8 -*-
# GENOCIDE - the king of the netherlands commits genocide
#
#

__version__ = 11

import doctest, os, sys, unittest

curdir = os.getcwd()
sys.path.insert(0, curdir + os.sep)
sys.path.insert(0, curdir + os.sep + ".." + os.sep)

#from PSphinxTheme.utils import set_psphinxtheme

# -- Options for GENERIC output ---------------------------------------------

project = "genocide"
master_doc = 'index'
version = '%s' % __version__
release = '%s' % __version__
language = ''
today = ''
today_fmt = '%B %d, %Y'
#needs_sphinx='1.1'
needs_sphinx='2.0'
exclude_patterns = ['_build', '_templates', '_source', 'Thumbs.db', '.DS_Store']
#exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
#default_role = ''
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
modindex_common_prefix = [""]
keep_warnings = True
templates_path=['_templates']
add_function_parentheses = True
add_module_names = False
show_authors = False
pygments_style = 'sphinx'

extensions=[
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    #'rst2pdf.pdfbuilder',
    #"sphinx_rtd_theme",
    #'PSphinxTheme.ext.psphinx_admonitions',
    #'PSphinxTheme.ext.escaped_samp_literals',
    #'PSphinxTheme.ext.index_styling',
    #'PSphinxTheme.ext.issue_tracker',
    #'PSphinxTheme.ext.sidebarlogo_perpag',
    #'PSphinxTheme.ext.relbar_links',
    #'PSphinxTheme.ext.table_styling'
]

# -- Options for HTML output -------------------------------------------------

#html_theme_path = []
#html_theme= "sphinx-material"
#html_theme = "alabaster"
html_theme = "haiku"
#html_theme="p-red",
#html_theme="pyramid"
#html_theme="yeen"
#html_theme_path, html_theme, needs_sphinx = set_psphinxtheme('p-red')
#html_theme="bizstyle"
#html_short_title = "GENOCIDE %s | OTP-CR-117/19/001" % __version__
html_short_title = ""
html_favicon = "genocidesmile.png"
#html_static_path = ["_static"]
html_extra_path = []
html_last_updated_fmt = '%Y-%b-%d'
html_additional_pages = {}
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
html_copy_source = False
html_use_opensearch = 'http://genocide.rtfd.io/'
html_file_suffix = '.html'
htmlhelp_basename = 'testdoc'
#html_theme_options = { "lighter_decor": True }
#html_logo = os.path.join('_static', 'P-SphinxTheme180_95_logo.png')
#html_favicon = os.path.join('_static', 'P-Projects32_32.ico')
#relbar_links_doc = [
#   ('toc', 'contents'),
#   ('api', 'api'),
#]
#sidebarlogo_perpage_dict = {
#   None: ['api', 'index', 'copyright'],
#   'P-SphinxTheme180_95_bg.png': ['main_theme', 'history'],
#}
#common_sidebars = ['quicklinks.html', 'sourcelink.html', 'searchbox.html']
#common_sidebars = ['searchbox.html', 'sourcelink.html']
#html_sidebars = {
#   '**': ['localtoc.html', 'relations.html'] + common_sidebars,
#   'py-modindex': common_sidebars,
#   'genindex': common_sidebars,
#   'search': common_sidebars,
#}

rst_prolog = """.. image:: genocideline2.png
    :height: 2.7cm
    :width: 15.7cm

.. title:: OTP-CR-117/19/001
"""

#rst_epilog=""".. raw:: pdf
#
#   PageBreak
#"""

intersphinx_mapping = {
                       'python': ('https://docs.python.org/3', 'objects.inv'),
                       'sphinx': ('http://sphinx.pocoo.org/', None),
                      }
intersphinx_cache_limit=1


# -- Options for CODE output -------------------------------------------------

autosummary_generate=True
autodoc_default_flags=['members', 'undoc-members', 'private-members', "imported-members"]
#autodoc_member_order='alphabetical'
autodoc_member_order='groupwise'
autodoc_docstring_signature=True
autoclass_content="class"
doctest_global_setup=""
doctest_global_cleanup=""
doctest_test_doctest_blocks="default"
trim_doctest_flags=True
doctest_flags=doctest.REPORT_UDIFF

nitpick_ignore=[
                ('py:class', 'builtins.BaseException'),
               ]


# -- Options for LATEX output -------------------------------------------------

latex_documents = [
    (master_doc, 'genocide.tex', u'genocide',
     u'Bart Thate', 'manual'),
]
latex_engine = 'pdflatex'
latex_elements = {
    'extraclassoptions': 'openany,oneside',
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'figure_align': 'htbp',
    'fontpkg': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
}

latex_show_urls = 'footnote'
latex_theme = "manual"
latex_elements = {
}

# -- Options for PDF output --------------------------------------------------

pdf_documents = [('index', u'genocide', u'genocide', u'Bart Thate'),]
#pdf_stylesheets = ['sphinx','kerning','a4']
#pdf_style_path = ['.', '_styles']
pdf_compressed = False
#pdf_font_path = ['/usr/share/fonts', '/usr/share/texmf-dist/fonts/']
pdf_language = "en_US"
pdf_fit_mode = "shrink"
pdf_break_level = 1
pdf_breakside = 'any'
pdf_inline_footnotes = True
pdf_use_index = True
pdf_use_modindex = True
pdf_use_coverpage = True
pdf_cover_template = 'sphinxcover.tmpl'
pdf_appendices = []
pdf_splittables = False
pdf_default_dpi = 72
pdf_extensions = []
pdf_page_template = 'cutePage'
pdf_use_toc = True
pdf_toc_depth = 9999
pdf_use_numbered_links = False
pdf_fit_background_mode = 'scale'
epub_copyright="Public Domain"
 