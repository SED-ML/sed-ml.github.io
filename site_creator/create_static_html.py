"""
Static site creator for sed-ml.org
"""
from pathlib import Path
import codecs
import os
from jinja2 import Environment, FileSystemLoader
import natsort
import requests
import yaml

TEMPLATE_DIR = Path(__file__).parent / 'templates'

# FIXME: autodetect all html files
SITES = [
    'index.html',
    'about.html',
    'contact.html',
    'examples.html',
    'publications.html',
    'showcase.html',
    'specifications.html',
    'urns.html',
    'notes.html'
]


def read_yaml(name: str, directory="./templates/db"):
    """ Read yaml data.

        'speakers' : ordered list of upcoming speakers (next to last)
        'talks' : ordered list of past talks (last to first)
        'alumnis': list of alumnis

    :param name: name of the yaml file, equal to content
    :param directory: base directory for yaml
    :return:
    """
    path = os.path.join(directory, '{}.yaml'.format(name))
    stram = open(path, "r")
    data = yaml.load(stram, Loader=yaml.FullLoader)
    return data[name]


PUBLICATIONS = read_yaml("publications")
EDITORS = read_yaml("editors")
EDITORS_ACTIVE = [e for e in EDITORS if e['active'] is True]
NEWS = read_yaml("news")
PRESENTATIONS = read_yaml("presentations")
LIBRARIES = read_yaml("libraries")
TOOLS = read_yaml("tools")
LANGUAGES = sorted(read_yaml("languages"), key=lambda l: l['language'])
SYMBOLS = read_yaml("symbols")
FORMATS = sorted(read_yaml("formats"), key=lambda f: f['format'])
UML_DIAGRAMS = read_yaml("uml_diagrams")
EXAMPLES = read_yaml("examples")


response = requests.get('https://api.biosimulators.org/simulators/latest')
response.raise_for_status()
simulators_specs = {simulator['id']: simulator for simulator in response.json()}

with open(os.path.join(os.path.dirname(__file__), '..', 'examples', 'simulator-compatibility.yml'), 'r') as file:
    example_simulator_compatibility = {example['filename']: example for example in yaml.load(file, Loader=yaml.FullLoader)}
for example in EXAMPLES:
    example['verifiedSimulators'] = []
    for simulator in example_simulator_compatibility[example['filename']]['simulators']:
        if simulator.get('notImplemented', None) is None:
            simulator_id = simulator['id']
            simulator_specs = simulators_specs[simulator_id]
            simulator_version = simulator_specs['version']
            simulator_name = simulator_specs['name']
            example['verifiedSimulators'].append({
                'id': simulator_id,
                'name': simulator_name,
                'version': simulator_version,
                'url': 'https://biosimulators.org/simulators/{}'.format(simulator_id)
            })
    natsort.natsorted(example['verifiedSimulators'], key=lambda simulator: simulator['id'])


def create_site(template="index.html", out_dir="../"):
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
                      trim_blocks=True,
                      lstrip_blocks=True)
    template = env.get_template(html_template)

    # Context
    c = {
        'data': 'data',
        'publications': PUBLICATIONS,
        'editors': EDITORS,
        'editors_active': EDITORS_ACTIVE,
        'news': NEWS,
        'presentations': PRESENTATIONS,
        'libraries': LIBRARIES,
        'tools': TOOLS,
        'languages': LANGUAGES,
        'symbols': SYMBOLS,
        'formats': FORMATS,
        'uml_diagrams': UML_DIAGRAMS,
        'examples': EXAMPLES,
    }
    return template.render(c)


def create_sites(out_dir="../"):
    print('-'*80)
    print('Creating static site from templates')
    print('-'*80)
    for site in SITES:
        create_site(template=site, out_dir=out_dir)


if __name__ == "__main__":
    create_sites(out_dir="../")
