from typing import List, Optional
from dataclasses import dataclass
from docstring_parser.common import Docstring


@dataclass
class Node:
    """Documentation for an AST node"""

    name: str
    qualified_name: str
    docstring: Optional[Docstring]
    raw_docstring: Optional[Docstring]

    @property
    def is_documented(self) -> bool:
        return self.raw_docstring is None


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
