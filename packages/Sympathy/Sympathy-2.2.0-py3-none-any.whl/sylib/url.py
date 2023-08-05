# This file is part of Sympathy for Data.
# Copyright (c) 2018 Combine Control Systems AB
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
import urllib.parse
import requests
import tempfile
from sympathy.api import exceptions


def download_datasource(datasource, filename=None, tempfile_kwargs=None):
    assert filename or tempfile_kwargs
    if datasource.decode_type() == datasource.modes.url:
        url = datasource['path']
        scheme = urllib.parse.urlparse(url).scheme
        if scheme in ['http', 'https']:
            headers = datasource['env']
            r = requests.get(url, headers=headers)

            if r.status_code != requests.codes.ok:
                raise exceptions.SyDataError(
                    'Failed, getting optaining the requested data')

            if filename:
                file_obj = open(filename, 'w+b')
            elif tempfile_kwargs:
                file_obj = tempfile.NamedTemporaryFile(
                    delete=False, **tempfile_kwargs)

            with file_obj as http_temp:
                for chunk in r.iter_content(chunk_size=1024):
                    http_temp.write(chunk)

            result_filename = http_temp.name
            datasource = type(datasource)()
            datasource.encode_path(result_filename)
        else:
            raise exceptions.SyDataError(
                "Datasource URL contains unhandled scheme: {}. "
                "Currently, http and https are supported.".
                format(scheme))
    return datasource
