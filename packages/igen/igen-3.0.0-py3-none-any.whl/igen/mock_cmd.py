# coding=utf-8

import re
from jinja2 import Environment, PackageLoader
from .pb import pasteboard_write
from .command import Command
from .constants import SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES
from .str_helpers import upper_first_letter


class MockCommand(Command):
    def __init__(self, protocol_text):
        super(MockCommand, self).__init__()
        self.protocol_text = protocol_text

    def create_mock(self, print_result):
        output = Mock(self.protocol_text).create_mock()
        if print_result:
            print()
            print(output)
            print()
        pasteboard_write(output)
        print('The result has been copied to the pasteboard.')


class Mock(object):

    class Function(object):
        def __init__(self, origin, name, params, return_type):
            super(Mock.Function, self).__init__()
            self.origin = origin
            self.name = name
            self.params = list(filter(None, params.split(',')))
            self.return_type = return_type
            self.is_overloaded = False

        def __str__(self):
            return self.origin

        @property
        def return_value(self):
            if self.return_type is None:
                return_value = '()'
            elif self.return_type.endswith('?'):
                return_value = 'nil'
            elif self.return_type.startswith('Driver'):
                regex = re.compile('Driver<(.+)>')
                mo = regex.search(self.return_type)
                observable_type = mo.group(1)
                if observable_type in SWIFT_TYPES:
                    return_value = 'Driver.just({})'.format(
                        SWIFT_TYPES_DEFAULT_VALUES[observable_type]
                    )
                else:
                    return_value = 'Driver<{}>.empty()'.format(observable_type)
            elif self.return_type.startswith('Observable'):
                regex = re.compile('Observable<(.+)>')
                mo = regex.search(self.return_type)
                observable_type = mo.group(1)
                if observable_type in SWIFT_TYPES:
                    return_value = 'Observable.just({})'.format(
                        SWIFT_TYPES_DEFAULT_VALUES[observable_type]
                    )
                else:
                    return_value = 'Observable<{}>.empty()'.format(
                        observable_type
                    )
            elif self.return_type in SWIFT_TYPES:
                return_value = SWIFT_TYPES_DEFAULT_VALUES[self.return_type]
            else:
                return_value = '{}()'.format(self.return_type)
            return return_value

        @property
        def return_void(self):
            return self.return_type is None

        @property
        def return_nil(self):
            return self.return_value == 'nil'

        @property
        def first_param(self):
            if self.params:
                param = self.params[0]
                param_name = param.split(':')[0].split(' ')
                return param_name[0] \
                    + "".join(x.title() for x in param_name[1:])
            return None

        @property
        def first_param_title(self):
            if self.first_param is not None:
                return upper_first_letter(self.first_param)
            return None

        @property
        def overloaded_name(self):
            if self.is_overloaded and (self.first_param_title is not None):
                return self.name + self.first_param_title
            return self.name

    def __init__(self, protocol_text):
        super(Mock, self).__init__()
        self.protocol_text = protocol_text

    def _get_protocol_name(self, str):
        regex = re.compile(r'protocol (\w+)')
        mo = regex.search(str)
        protocol_name = mo.group(1)
        if protocol_name.endswith('Type'):
            class_name = protocol_name[:-4]
        elif protocol_name.endswith('Protocol'):
            class_name = protocol_name[:-8]
        else:
            class_name = protocol_name
        return (protocol_name, class_name)

    def create_mock(self):
        str = self.protocol_text
        is_protocol = False
        protocol_name = ''
        class_name = ''
        # get protocol name
        try:
            (protocol_name, class_name) = self._get_protocol_name(str)
            is_protocol = True
        except Exception:
            pass
        # get functions
        func_regex = re.compile(r'func (\w+)\((.*)\)( -> (.*))?')
        funcs = [Mock.Function(f.group(), f.group(1), f.group(2), f.group(4))
                 for f in func_regex.finditer(str)]

        if not funcs:
            print('The protocol or functions in the pasteboard is invalid.')
            exit(1)

        # check if overloaded
        func_dict = {}
        for f in funcs:
            if f.name in func_dict:
                func_dict[f.name] = func_dict[f.name] + 1
            else:
                func_dict[f.name] = 1
        for f in funcs:
            f.is_overloaded = func_dict[f.name] > 1

        env = Environment(
            loader=PackageLoader('igen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template("Mock.swift")
        content = template.render(
            class_name=class_name,
            protocol_name=protocol_name,
            functions=funcs,
            is_protocol=is_protocol
        )
        return content
