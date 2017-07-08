"""
Static site creator for sed-ml.org
"""
from __future__ import print_function, absolute_import
import codecs
import os
import warnings
from jinja2 import Environment, FileSystemLoader

# template location
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
SITES = ['index.html',
         'about.html',
         'contact.html',
         'documents.html',
         'examples.html',
         'publications.html',
         'showcase.html',
         'specifications.html',
         ]


def create_site(template="index.html", out_dir="_site"):
    """ Creates site from given template. """

    # write html (unicode)
    html = _create_html(html_template=template)
    f_html = codecs.open(os.path.join(out_dir, template), encoding='utf-8', mode='w')
    f_html.write(html)
    f_html.close()


def _create_html(html_template='report.html'):
    """Create HTML from SBML.

    :param doc:
    :type doc:
    :param html_template:
    :type html_template:
    :return:
    :rtype:
    """
    # template environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                      extensions=['jinja2.ext.autoescape'],
                      trim_blocks=True,
                      lstrip_blocks=True)
    template = env.get_template(html_template)
    # Context
    c = {
        'data': 'data'
    }
    return template.render(c)


def create_sites():
    print('-'*80)
    print('Creating static site from templates')
    print('-'*80)
    for site in SITES:
        create_site(template=site, out_dir="_site")


if __name__ == "__main__":
    create_sites()
