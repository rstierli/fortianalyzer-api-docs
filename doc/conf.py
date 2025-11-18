# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
from datetime import date

# load variables from the config file
PROJECT_ENV="../config/project.env"

from dotenv import dotenv_values
config = dotenv_values(PROJECT_ENV)

# project name can be changed after initial setup and for PDF generation (escape underscores for latex )
project_name = config.get('PROJECT_NAME').strip('"')
project_long_name = config.get('PROJECT_LONG_NAME').strip('"')
copyright_owner = os.getenv("COPYRIGHT", "").replace('"', '')
copyright = f"{date.today().year}, {copyright_owner}"
author = config.get('AUTHOR').strip('')
version = config.get('MAJOR_VERSION').strip('"')
release = config.get('FULL_RELEASE_VERSION').strip('"')
title_under_logo = config.get('TITLE_UNDER_LOGO').strip('"')
light_mode_logo = config.get('LIGHT_MODE_LOGO').strip('"')
dark_mode_logo = config.get('DARK_MODE_LOGO').strip('"')
right_sidebar_toc_title = config.get('RIGHT_SIDEBAR_TOC_TITLE').strip('"')

html_last_updated_fmt = ""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_copybutton',
    'sphinxcontrib.lightbox2',
    'sphinx.ext.autosectionlabel',
    'sphinx_toolbox.collapse',
    'sphinx_togglebutton',
    'sphinx_design',
    'myst_parser' # enable myst parser
]

myst_enable_extensions = [
    "substitution",
]

# autosectionlabel configuration - prefix document name to avoid duplicate labels
autosectionlabel_prefix_document = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv', 'INSTALL','README.md','CHANGELOG.md']

# Recognize both .rst and .md files as source files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

# Add any paths that contain custom static files (such as style sheets) 
# here, relative to this directory. They are copied after the builtin 
# static files, so a file named "default.css" will overwrite the builtin 
# "default.css".

html_theme_options = {
    #"announcement": project_name,
    "logo": {
        "text": title_under_logo,
        "image_light": html_static_path[0] + "/" + light_mode_logo,
        "image_dark": html_static_path[0] + "/" + dark_mode_logo,
    },
    "show_toc_level": 5,
    "show_nav_level": 5,
    "toc_title": right_sidebar_toc_title,
}

# Change |project_name| in index.rst 

rst_prolog = f'''
.. |project_name| replace:: {project_long_name}
'''

# Change |project_name| in index.md
myst_substitutions = {
    "project_name": project_long_name,
}

# -- LaTeX output configuration ----------------------------------------------
latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'sphinxsetup': 'TitleColor={RGB}{35,96,147},InnerLinkColor={RGB}{35,96,147},OuterLinkColor={RGB}{35,96,147}',

    'preamble': r"""
    % remove chapter headers    
    \usepackage{titlesec}
    \titleformat{\chapter}{}{}{0em}{\bf\LARGE}
    \setlength{\headheight}{14.5pt}
    \usepackage{tikz}
    \usepackage{xcolor}
    \usepackage{geometry}
    \usepackage[titles]{tocloft}
    \renewcommand{\cftsecfont}{\normalfont\bfseries}
    \renewcommand{\cftsecpagefont}{\normalfont\bfseries}
    \renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
    \setlength{\cftbeforesecskip}{0.5em}
    \setlength{\cftaftertoctitleskip}{1em}
    \cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
    \setlength{\cftchapnumwidth}{0.75cm}
    \setlength{\cftsecindent}{\cftchapnumwidth}
    \setlength{\cftsecnumwidth}{1.25cm}

    % Set Fortinet Fonts
    \usepackage{fontspec}
    \setmainfont{Helvetica Neue LT Pro}[
    UprightFont = "HelveticaNeueLTProLt",
    ItalicFont = "HelveticaNeueLTProLtIt",
    BoldFont = "HelveticaNeueLTProBd",
    BoldItalicFont = "HelveticaNeueLTProBdIt",
    Extension = .otf,
    Path = /home/sphinx/.fonts/
]

% Custom page geometry
\geometry{top=2.5cm, bottom=2.5cm, left=1.5cm, right=1.5cm}

% reduce space before chapter title
\titlespacing{\chapter}{0pt}{-32pt}{1cm} 

% Redefine the title page with a background image
\makeatletter
\renewcommand{\maketitle}{
    \begin{titlepage}
        \begin{tikzpicture}[remember picture, overlay]
            % Add background image (adjust scale as needed)
            \node[anchor=south] at (current page.south) {%
                \includegraphics[width=\paperwidth]%
                {../../_static/background-image.png}};
            
            % Add Fortinet logo in the top-left corner
            \node[anchor=north west, yshift=-2cm, xshift=1.5cm] at (current page.north west) {%
                \includegraphics[height=5mm]{../../_static/light-fortinet-logo.png}};
        \end{tikzpicture}
        
        \vspace*{2cm}
        \begin{flushleft}
            {\Huge\textbf{\@title}}\\[1cm]
            {\Large\textbf{\@author}}\\[2cm]
        \end{flushleft}     
    \end{titlepage}
}
\makeatother
""",
    'maketitle': r'\maketitle',
    'tableofcontents': r'\tableofcontents',

}
# Additional latex configuration , get project name without escaping underscores this time
latex_documents = [
    ('index', f"{project_name}.tex", project_long_name,
     author, 'manual'),
]
# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = html_static_path[0] + "/" + light_mode_logo
latex_additional_files = ['../doc/_static/light-fortinet-logo.png']
