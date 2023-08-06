"""Setup for launchcontainer XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-launchcontainer',
    version='2.3.0',
    author='Bryan Wilson, Appsembler',
    description=('Open EdX XBlock to display a button allowing an LMS user '
                 'to launch and link to an external courseware resource via the '
                 'Wharf container API'),
    packages=[
        'launchcontainer',
    ],
    install_requires=[
        'XBlock',
        'django-crum'
    ],
    entry_points={
        'xblock.v1': [
            'launchcontainer = launchcontainer.launchcontainer:LaunchContainerXBlock',
        ]
    },
    package_data=package_data("launchcontainer", ["static", "public"]),
)
