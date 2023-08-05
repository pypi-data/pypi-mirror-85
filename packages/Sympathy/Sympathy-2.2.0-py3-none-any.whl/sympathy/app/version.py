# This file is part of Sympathy for Data.
# Copyright (c) 2013 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
from sympathy import version
from sympathy.utils import prim

major = version.major
minor = version.minor
micro = version.micro
status = version.status

version_tuple = version.version_tuple
version = version.version
build = status


def application_name():
    return 'Sympathy for Data'


def application_url():
    """Return the URL to the developer website."""
    return 'https://www.sympathyfordata.com/'


def documentation_url():
    """Return the URL to the documentation."""
    return f'https://www.sympathyfordata.com/doc/{major}.{minor}.{micro}/'


def application_copyright():
    """Return the name of the copyright holder."""
    return 'Combine Control Systems AB'


def email_bugs():
    """Return the email address for bug reports."""
    return 'support@sympathyfordata.com'


def email_contribution():
    """Return the email address to use for those who want to contribute."""
    return 'support@sympathyfordata.com'


def license_info():
    """Return a dict with info about the license."""
    return prim.config()['license']
