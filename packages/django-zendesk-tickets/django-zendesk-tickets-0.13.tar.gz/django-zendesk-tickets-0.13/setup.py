import importlib
import os

from setuptools import setup

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, 'README.rst')) as readme:
    README = readme.read()

install_requires = ['requests']
setup_requires = ['Django>=2.2,<4']
tests_require = ['flake8']
install_requires += setup_requires

package_info = importlib.import_module('zendesk_tickets')
setup_extensions = importlib.import_module('zendesk_tickets.setup_extensions')
command_classes = setup_extensions.command_classes.copy()

setup(
    name='django-zendesk-tickets',
    version=package_info.__version__,
    author=package_info.__author__,
    author_email='dev@digital.justice.gov.uk',
    url='https://github.com/ministryofjustice/django-zendesk-tickets',
    packages=['zendesk_tickets'],
    include_package_data=True,
    license='MIT',
    description='Django views and forms that submit tickets to Zendesk',
    long_description=README,
    keywords='zendesk django tickets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    cmdclass=command_classes,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests.run',
)
