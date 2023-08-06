# coding=utf-8

import re
from jinja2 import Environment, PackageLoader


class ViewModel(object):

    class Property(object):
        def __init__(self, name, type_name):
            super(ViewModel.Property, self).__init__()
            self.name = name
            self.type_name = type_name

        def __str__(self):
            return "let {}: Driver<{}>".format(self.name, self.type_name)

    def __init__(self, vm_text):
        super(ViewModel, self).__init__()
        self.vm_text = vm_text

    @property
    def view_model_name(self):
        try:
            regex = re.compile(r'(?:struct|extension) (\w+)ViewModel')
            mo = regex.search(self.vm_text)
            return mo.group(1)
        except Exception:
            print("The ViewModel in the pasteboard is invalid.")
            exit(1)

    @property
    def properties(self):
        try:
            str = self.vm_text

            # Input
            input_block_regex = re.compile("struct Input {([^}]+)")
            input_block = input_block_regex.search(str).group(1)
            input_properties_regex = re.compile(r'let (\w+): Driver<([^>]+)>')
            input_properties = [
                ViewModel.Property(p[0], p[1])
                for p in input_properties_regex.findall(input_block)
            ]

            # Output
            output_block_regex = re.compile("struct Output {([^}]+)")
            output_block = output_block_regex.search(str).group(1)
            output_properties_regex = re.compile(r'(?:let|var) (\w+)(?: =|:)(?:.*)')
            output_properties = [
                ViewModel.Property(p, 'Any')
                for p in output_properties_regex.findall(output_block)
            ]

            return (input_properties, output_properties)
        except Exception:
            print("The ViewModel in the pasteboard is invalid.")
            exit(1)


class UnitTest(ViewModel):

    def create_tests(self):
        input_properties, output_properties = self.properties
        env = Environment(
            loader=PackageLoader('igen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template("UnitTest.swift")
        content = template.render(
            name=self.view_model_name,
            input_properties=input_properties,
            output_properties=output_properties
        )
        return content


class BindViewModel(ViewModel):

    def create_bind_view_model(self):
        input_properties, output_properties = self.properties
        env = Environment(
            loader=PackageLoader('igen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template("BindViewModel.swift")
        content = template.render(
            name=self.view_model_name,
            input_properties=input_properties,
            output_properties=output_properties
        )
        return content
