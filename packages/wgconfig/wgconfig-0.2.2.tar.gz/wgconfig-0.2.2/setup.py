import os
import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setup_kwargs = {
    'name': 'wgconfig',
    'version': '0.2.2',
    'author': 'Dirk Henrici',
    'author_email': 'towalink.wgconfig@henrici.name',
    'description': 'parsing and writing WireGuard configuration files',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'url': 'https://www.github.com/towalink/wgconfig',
    'packages': setuptools.find_packages(),
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology'
    ],
    'python_requires': '>=2.7',
    'extras_require': {
        ':python_version == "2.7"': ['future']
    },
    'keywords': 'WireGuard configuration config wg',
    'project_urls': {
        'Repository': 'https://www.github.com/towalink/wgconfig',
        'PyPi': 'https://pypi.org/project/wgconfig/'
    },
}


if __name__ == '__main__':
    setuptools.setup(**setup_kwargs)
