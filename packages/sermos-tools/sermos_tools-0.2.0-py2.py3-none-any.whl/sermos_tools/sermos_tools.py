""" Core/base Sermos Tools classes
"""
import os
import re
import pkg_resources
from typing import List, Union
from sermos_tools.constants import BASE_CATALOG_DIR
from importlib import import_module


class SermosTool:
    """ Thin wrapper for standard tools available in Sermos Pipelines
    """
    @classmethod
    def name(cls):
        """ Return the tool's name, based on the Class Name
        """
        return cls.__name__


def is_capital_case(capital_case: str) -> bool:
    """ Test if string is CapitalCase
    """
    if re.match(r'^[A-Z][a-z]+(?:[A-Z][a-z]+)*$', capital_case):
        return True
    return False


def is_snake_case(snake_case: str) -> bool:
    """ Test if string is snake_case
    """
    if re.match(r'^([a-z0-9]+)(_([a-z0-9]+))?$', snake_case):
        return True
    return False


def capital_to_snake(capital_case: str):
    """ Convert CapitalCaseName to capital_case_name in snake_case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', capital_case).lower()


def snake_to_capital(snake_string: str) -> str:
    """ Accept a snake_case_string and return a CapitalCaseString
    """
    components = snake_string.split('_')
    components = [c.capitalize() for c in components]
    return "".join(components)


def list_available_tools(as_dict: bool = False) -> Union[List, dict]:
    """ List all available tools

        as_dict (bool): If True, return as dictionary with tool_name as key
            and tool path as value, e.g. {'tool': 'sermos_tools/catalog/tool'}
    """
    tools = {}
    sermos_tools_path = pkg_resources.resource_filename('sermos_tools', '')
    catalog_path = sermos_tools_path + '/catalog'
    dir_objects = os.listdir(catalog_path)
    for dir_object_name in dir_objects:
        if '__' in dir_object_name:
            continue
        tool_path = catalog_path + '/' + dir_object_name
        if os.path.isdir(tool_path):
            tools[dir_object_name] = tool_path
    if as_dict:
        return tools
    return list(tools.keys())


def retrieve_tool_class(tool_name: str) -> SermosTool:
    """ Given a tool_name, retrieve the ToolName class
    """
    tools = list_available_tools(as_dict=True)
    class_name = snake_to_capital(tool_name)
    tool_name = capital_to_snake(tool_name)  # Normalize

    # Normalize the full tool path (which is full path on filesystem) to a
    # module path, e.g.
    # /dist/sermos-tools/sermos_tools/catalog/bar -> sermos_tools.catalog.bar
    path_bits = tools[tool_name].split('/')
    module_path = ''
    for idx, bit in enumerate(path_bits):
        if bit == 'sermos_tools':
            module_path = '.'.join(path_bits[idx:])
            break

    imported_module = import_module(module_path)
    return getattr(imported_module, class_name)


class SermosTools:
    """ Basic class holding one or more SermosTool objects. Typical usage is
        inside the context of an application that wants access to a particular
        tool. This is useful if you want to have an in-memory cache of loaded
        tools that are used more than once vs instantiating the tool for each
        use. When using the .get() method it will load and cache on this object
        for future retrieval such that subsequent .get() calls pull from
        already instantiated tool, e.g.::

            tools = SermosTools()
            task_runner = tools.get('task_runner)
    """
    def set_tool(self, tool: SermosTool, init: bool = False, **kwargs):
        """ Set a Sermos Tool as an attribute on this wrapper. This can be
            useful for adding custom SermosTool objects, for example.

            init (bool): Whether to add the tool initialized with kwargs or
                to simply provide reference to the tool class.
        """
        if init:
            setattr(self, tool.name(), tool(**kwargs))
        else:
            setattr(self, tool.name(), tool)

    def get(self, tool_name: str, **kwargs) -> SermosTool:
        """ Get a Sermos Tool by name. Accepts CapitalCase and snake_case.

            tool_name (str): Name of the tool to retrieve and instantiate.
            kwargs: [Optional] Passed to tool during instantiation.
        """
        # If we've already loaded the tool, great, return.
        if getattr(self, tool_name, None) is not None:
            return getattr(self, tool_name)

        # If not, let's try to load it
        tool = retrieve_tool_class(tool_name)
        self.set_tool(tool)
        return tool

    @property
    def available_tools(self) -> List[str]:
        """ Return the list of tools available on this instance.
        """
        tools = []
        for attr in self.__dict__:
            if issubclass(getattr(self, attr), SermosTool):
                tools.append(attr)
        return tools
