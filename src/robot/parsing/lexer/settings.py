#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .tokens import Token


class Settings(object):
    names = ()
    aliases = {}
    multi_use = ()

    def __init__(self):
        self.settings = {n: False for n in self.names}

    def tokenize(self, statement):
        name = self._format_name(statement[0].value)
        upper = name.upper()    # TODO: Non-ASCII spaces
        if upper in self.aliases:
            upper = self.aliases[upper]
        # TODO: Error reporting
        if upper not in self.settings:
            return Token.ERROR
            raise ValueError("Invalid setting '%s'." % name)  # TODO: Hints?
        if self.settings[upper] and upper not in self.multi_use:
            return Token.ERROR
            raise ValueError("Setting '%s' allowed only once." % name)
        self.settings[upper] = True
        return getattr(Token, upper.replace(' ', '_'))

    def _format_name(self, name):
        return name


class TestCaseFileSettings(Settings):
    # FIXME: Non-ASCII spaces
    names = (
        'DOCUMENTATION',
        'SUITE SETUP',
        'SUITE TEARDOWN',
        'METADATA',
        'TEST SETUP',
        'TEST TEARDOWN',
        'TEST TEMPLATE',
        'TEST TIMEOUT',
        'FORCE TAGS',
        'DEFAULT TAGS',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )
    aliases = {
        'TASK SETUP': 'TEST SETUP',
        'TASK TEARDOWN': 'TEST TEARDOWN',
        'TASK TEMPLATE': 'TEST TEMPLATE',
        'TASK TIMEOUT': 'TEST TIMEOUT',
    }
    multi_use = (
        'METADATA',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )


# FIXME: Implementation missing. Need to check what settings are supported.
class InitFileSettings(Settings):
    pass


class ResourceFileSettings(Settings):
    names = (
        'DOCUMENTATION',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )
    multi_use = (
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )


class TestCaseSettings(Settings):
    names = (
        'DOCUMENTATION',
        'SETUP',
        'TEARDOWN',
        'TEMPLATE',
        'TIMEOUT',
        'TAGS'
    )

    def __init__(self, parent):
        Settings.__init__(self)
        self.parent = parent

    def _format_name(self, name):
        return name[1:-1].strip()

    @property
    def template_set(self):
        # FIXME: Should look at the values as well
        return (self.settings['TEMPLATE'] or
                self.parent.settings['TEST TEMPLATE'])


class KeywordSettings(Settings):
    names = (
        'DOCUMENTATION',
        'ARGUMENTS',
        'TEARDOWN',
        'TIMEOUT',
        'TAGS',
        'RETURN'
    )

    def _format_name(self, name):
        return name[1:-1].strip()
