from __future__ import unicode_literals

import io
import sys

import six
from nose.plugins import Plugin
from nose.plugins.capture import Capture

from allura.lib.helpers import monkeypatch


# from https://github.com/asottile/behave/commit/384b028018996728318c508d5acb702c92e81a95
class CaptureIO(io.TextIOWrapper):
    def __init__(self):
        super(CaptureIO, self).__init__(
            io.BytesIO(),
            encoding='UTF-8', newline='', write_through=True,
        )

    def getvalue(self):
        return self.buffer.getvalue().decode('UTF-8')


class MonkeyPatchCapture(Plugin):
    """
    This doesn't do anything as a plugin itself.
    It is used to hook into nose execution very early, before the default "capture" plugin starts
    We replace its start() method which uses StringIO and suffers from:
        AttributeError: '_io.StringIO' object has no attribute 'buffer'
        https://github.com/nose-devs/nose/issues/1098
        due to mercurial accessing sys.stdout.buffer which normal python3 stdout has
    This new version uses a CaptureIO class which includes a .buffer attr
    """
    enabled = False

    def __init__(self):
        super(MonkeyPatchCapture, self).__init__()

        if six.PY3:
            @monkeypatch(Capture)
            def start(self):
                self.stdout.append(sys.stdout)
                self._buf = CaptureIO()
                sys.stdout = self._buf