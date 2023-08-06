'''
This file is part of pyRFXtrx, a Python library to communicate with
the RFXtrx family of devices from http://www.rfxcom.com/
See https://github.com/Danielhiversen/pyRFXtrx for the latest version.

Copyright (C) 2012  Edwin Woudt <edwin@woudt.nl>

pyRFXtrx is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyRFXtrx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyRFXtrx.  See the file COPYING.txt in the distribution.
If not, see <http://www.gnu.org/licenses/>.
'''

from setuptools import setup

setup(
#    name = 'pyRFXtrx',
    name='pyRFXtrx-tipi85',
    packages = ['RFXtrx'],
    install_requires=['pyserial>=2.7'],
#    version = '0.26.0',
    version = '0.25.9',
    description = 'a library to communicate with the RFXtrx family of devices',
    author='Edwin Woudt',
    author_email='edwin@woudt.nl',
#    url='https://github.com/Danielhiversen/pyRFXtrx',
    url='https://github.com/tipi85/pyRFXtrx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
