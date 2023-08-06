from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from docstring_parser.common import Docstring
from jinja2 import Template
import typer

from .helpers import resolve_doc_file_path


@dataclass
class Node:
    """Documentation for an AST node"""

    name: str
    qualified_name: str
    docstring: Optional[Docstring]
    raw_docstring: Optional[Docstring]


@dataclass
class FuncDef(Node):
    """Documentation for a function or method definition"""

    source: Optional[str]


@dataclass
class ClassDef(Node):
    """Representation of docstrings """

    source: Optional[str]
    methods: List[FuncDef]


@dataclass
class Module(Node):
    """Representation of docstrings and metadata contained in a module"""

    classes: List[ClassDef]
    functions: List[FuncDef]


@dataclass
class Package:
    """Representation of docstrings and metadata contained in a Package"""

    name: str
    modules: List[Module]

    def render(self, template: Template) -> str:
        """Render a template with the package"""
        return template.render(package=self)

    def render_modules(self, template: Template) -> Dict[str, str]:
        """Render a template for each module"""
        return {
            module.qualified_name: template.render(module=module)
            for module in self.modules
        }


class OutputMode(Enum):
    """How and where to render and write documentation
    OutputMode.file: render documentation for the entire package in a singe file.
        The template receives a Package instance
    OutputMode.stdout: same as OutputModel.file, but write to standard output instead
    OutputMode.directory: render documentation in one file per module, where the
        package structure is preserved
    """

    file = "file"
    directory = "directory"
    stdout = "stdout"

    def _write_to_stdout(self, package: Package, template: Template):
        typer.echo(package.render(template))

    def _write_to_file(self, package: Package, template: Template, output: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w") as output_file:
            output_file.write(package.render(template))

    def _write_to_dir(
        self, package: Package, template, output: Path, file_extension: str
    ):
        rendered_modules = package.render_modules(template)
        for module_name, content in rendered_modules.items():
            doc_file_path = resolve_doc_file_path(module_name, output, file_extension)
            doc_file_path.parent.mkdir(parents=True, exist_ok=True)
            with doc_file_path.open("w") as output_file:
                output_file.write(content)

    def apply(self, package: Package, output: Path, template_file: Path):
        """Render and write documentation according to the output mode

        Args:
            package (Package): [description]
            output (Path): [description]
            template_file (Path): [description]
        """
        with template_file.open("r") as file:
            template = Template(file.read())

        if self is OutputMode.stdout:
            self._write_to_stdout(package, template)
        elif self is OutputMode.file:
            self._write_to_file(package, template, output)
        elif self is OutputMode.directory:
            self._write_to_dir(
                package, template, output, "".join(template_file.suffixes)
            )
