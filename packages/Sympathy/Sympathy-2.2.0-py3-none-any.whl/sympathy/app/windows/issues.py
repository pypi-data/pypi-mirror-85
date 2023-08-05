# This file is part of Sympathy for Data.
# Copyright (c) 2019 Combine Control Systems AB
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
import Qt.QtWidgets as QtWidgets
import Qt.QtCore as QtCore
import platform
import os
import json
import requests
import logging
from sympathy.utils import pip_util
import sympathy.app.settings
import sympathy.app.version
import sympathy.app.user_statistics

core_logger = logging.getLogger('core')


def _info_form_layout():
    layout = QtWidgets.QFormLayout()
    layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
    layout.setFormAlignment(QtCore.Qt.AlignLeft)
    layout.setLabelAlignment(QtCore.Qt.AlignVCenter)
    layout.setVerticalSpacing(15)
    return layout


class SystemInfo(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = _info_form_layout()

        self._system = QtWidgets.QLineEdit(platform.system())
        self._machine = QtWidgets.QLineEdit(platform.machine())
        self._release = QtWidgets.QLineEdit(platform.release())
        self._version = QtWidgets.QLineEdit(platform.version())
        self._processor = QtWidgets.QLineEdit(platform.processor())

        layout.addRow('System', self._system)
        layout.addRow('Machine', self._machine)
        layout.addRow('Release', self._release)
        layout.addRow('Version', self._version)
        layout.addRow('Processor', self._processor)

        self.setLayout(layout)

    def to_dict(self):
        return {
            'system': self._system.text(),
            'machine': self._machine.text(),
            'system_release': self._release.text(),
            'system_version': self._version.text(),
            'processor': self._processor.text()
        }


def packages():
    # Use common utility from pip util with shared global store.
    required_file = os.path.join(
        sympathy.app.settings.instance()['install_folder'], 'Package', 'requires.txt')
    required = pip_util.requirements(required_file).keys()
    installed = pip_util.freeze()
    return '\n'.join(
        [f'{k} == {v}' for k, v in installed.items() if k in required])


class PythonInfo(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = _info_form_layout()

        self._python_version = QtWidgets.QLineEdit(platform.python_version())
        self._architecture = QtWidgets.QLineEdit(platform.architecture()[0])
        self._sympathy_version = QtWidgets.QLineEdit(sympathy.app.version.version)
        self._packages = QtWidgets.QTextEdit()
        self._packages.setPlainText(packages())

        policy = self._packages.sizePolicy()
        policy.setVerticalStretch(1)
        self._packages.setSizePolicy(policy)

        layout.addRow('Python Version', self._python_version)
        layout.addRow('Architecture', self._architecture)
        layout.addRow('Sympathy Version', self._sympathy_version)
        layout.addRow('Packages', self._packages)

        self.setLayout(layout)

    def to_dict(self):
        return {
            'python_version': self._python_version.text(),
            'python_architecture': self._architecture.text(),
            'sympathy_version': self._sympathy_version.text(),
            'python_packages': pip_util.freeze_from_str(
                self._packages.toPlainText())
        }


class IssueMessage(QtWidgets.QWidget):

    def __init__(self, subject=None, details=None, generated=False,
                 parent=None):
        super().__init__(parent=parent)

        layout = _info_form_layout()
        subject = subject or ''
        details = details or ''

        if generated:
            details = '\n'.join([
                '[Automatically generated report, please ensure that no '
                'personal or sensitive information is included]\n',
                details])

        self._subject = QtWidgets.QLineEdit()
        self._subject.setText(subject)
        self._subject.setPlaceholderText('Enter subject for issue')
        self._details = QtWidgets.QTextEdit()
        self._details.setPlainText(details)

        detail_info = """Enter description for issue.
- Steps to reproduce.
- Expected behavior compared to actual.

Please ensure that no personal or sensitive information is included.
"""

        self._details.setToolTip(detail_info)
        self._details.setPlaceholderText(detail_info)

        policy = self._details.sizePolicy()
        policy.setVerticalStretch(1)
        self._details.setSizePolicy(policy)

        layout.addRow('Subject', self._subject)
        layout.addRow('Details', self._details)

        self.setLayout(layout)

    def to_dict(self):
        return {
            'subject': self._subject.text(),
            'details': self._details.toPlainText()
        }


class IssueReport(QtWidgets.QWidget):

    def __init__(self, subject=None, details=None, generated=False,
                 parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QVBoxLayout()
        tabs = QtWidgets.QTabWidget()
        self._issue = IssueMessage(
            subject=subject, details=details, generated=generated)
        self._python = PythonInfo()
        self._system = SystemInfo()

        tabs.addTab(self._issue, 'Issue')
        tabs.addTab(self._python, 'Python')
        tabs.addTab(self._system, 'System')

        layout.addWidget(tabs)
        self.setLayout(layout)

    def to_dict(self):
        python_dict = dict(self._python.to_dict())
        python_packages = python_dict.pop('python_packages')
        system_dict = self._system.to_dict()

        return {
            'issue': self._issue.to_dict(),
            'python': python_dict,
            'python_hash': sympathy.app.user_statistics.basic_hash(python_dict),
            'python_packages': python_packages,
            'python_packages_hash': sympathy.app.user_statistics.basic_hash(
                python_packages),
            'system': system_dict,
            'system_hash': sympathy.app.user_statistics.basic_hash(system_dict)
        }


class SenderThread(QtCore.QThread):
    succeeded = QtCore.Signal(bool)

    def __init__(self, url, headers, data, timeout, parent=None):
        self._url = url
        self._headers = headers
        self._data = data
        self._timeout = timeout
        super().__init__(parent=parent)

    def run(self):
        try:
            r = requests.post(
                url=self._url,
                data=json.dumps(self._data),
                headers=self._headers,
                timeout=self._timeout)

            self.succeeded.emit(r.status_code == requests.codes.ok)
        except Exception as e:
            core_logger.info(
                'Failed sending user statistics to %s.: %s', self._url, e)

            self.succeeded.emit(False)


class IssueReportSender(QtWidgets.QDialog):
    finished = QtCore.Signal()

    def __init__(self, subject=None, details=None, generated=False,
                 parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Create new issue')
        layout = QtWidgets.QVBoxLayout()
        self._issues = IssueReport(
            subject=subject, details=details, generated=generated)
        buttons = QtWidgets.QDialogButtonBox()
        layout.addWidget(self._issues)
        layout.addWidget(buttons)

        self._send = QtWidgets.QPushButton('Send')
        buttons.addButton(self._send,
                          QtWidgets.QDialogButtonBox.ActionRole)

        cancel = buttons.addButton(QtWidgets.QDialogButtonBox.Cancel)

        self._send.clicked.connect(self._send_issue_report)
        cancel.clicked.connect(self.reject)

        self.setLayout(layout)
        self.save()

    def save(self):
        self._data = self._issues.to_dict()

    def _send_issue_report(self):
        self._send.setText('Sending...')
        self._send.setEnabled(False)
        new_data = self._issues.to_dict()
        res = {}

        for k, v in new_data.items():
            modified = self._data[k] != v
            res[f'{k}_modified'] = modified
            res[k] = v

        self._sender = SenderThread(
            f'{sympathy.app.user_statistics.api_url()}/issue/',
            headers=sympathy.app.user_statistics.api_headers(),
            data=res,
            timeout=2.0)

        self._sender.finished.connect(self._sender_finished)
        self._sender.succeeded.connect(self._sender_succeeded)
        self._sender.start()

    def _sender_succeeded(self, ok):
        if ok:
            self.accept()
        else:
            self._send.setText('Failed, retry sending?')
            self._send.setEnabled(True)

    def _sender_finished(self):
        self._sender.wait()
        self._sender = None
