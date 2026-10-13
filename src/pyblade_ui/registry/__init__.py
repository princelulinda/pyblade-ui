"""The registry: the catalogue of components and the files each one is made of.

A registry is a `registry.json` next to the files it lists, wherever that is:
the folder bundled with this package, another folder, or a URL (a GitHub raw
URL works). Paths in the registry are relative to it, and are also where a file
lands in the project's components directory: `ui/button.html` is installed as
`components/ui/button.html` and used as `<pb-ui.button>`.
"""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

BUNDLED = Path(__file__).parent
ITEM_TYPES = {"registry:ui", "registry:block", "registry:lib"}


class RegistryError(Exception):
    pass


@dataclass
class Item:
    name: str
    type: str
    title: str
    description: str
    files: list[str]
    registry_dependencies: list[str] = field(default_factory=list)
    js: list[str] = field(default_factory=list)
    python: list[str] = field(default_factory=list)
    usage: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        dependencies = data.get("dependencies", {})
        return cls(
            name=data["name"],
            type=data.get("type", "registry:ui"),
            title=data.get("title", data["name"]),
            description=data.get("description", ""),
            files=list(data.get("files", [])),
            registry_dependencies=list(data.get("registryDependencies", [])),
            js=list(dependencies.get("js", [])),
            python=list(dependencies.get("python", [])),
            usage=data.get("usage", ""),
        )


class Registry:
    def __init__(self, source: str = ""):
        self.source = source or str(BUNDLED)
        self.remote = self.source.startswith(("http://", "https://"))
        data = json.loads(self._read("registry.json"))
        self.name = data.get("name", "registry")
        self.items: dict[str, Item] = {}
        for raw in data.get("items", []):
            item = Item.from_dict(raw)
            self.items[item.name] = item

    def _read(self, path: str) -> str:
        if self.remote:
            url = f"{self.source.rstrip('/')}/{path}"
            try:
                with urllib.request.urlopen(url, timeout=20) as response:
                    return response.read().decode("utf-8")
            except OSError as exc:
                raise RegistryError(f"Could not fetch {url}: {exc}") from exc

        file = Path(self.source) / path
        if not file.is_file():
            raise RegistryError(f"{file} does not exist")
        return file.read_text(encoding="utf-8")

    def read_file(self, path: str) -> str:
        return self._read(path)

    def get(self, name: str) -> Item:
        if name not in self.items:
            raise RegistryError(f"'{name}' is not in the {self.name} registry. Run `pyblade-ui list`.")
        return self.items[name]

    def resolve(self, names: list[str]) -> list[Item]:
        """The items asked for and everything they depend on, dependencies first."""
        ordered: list[Item] = []
        visiting: set[str] = set()
        done: set[str] = set()

        def visit(name: str):
            if name in done:
                return
            if name in visiting:
                raise RegistryError(f"Circular dependency on '{name}'")
            visiting.add(name)
            item = self.get(name)
            for dependency in item.registry_dependencies:
                visit(dependency)
            visiting.discard(name)
            done.add(name)
            ordered.append(item)

        for name in names:
            visit(name)
        return ordered

    def validate(self) -> list[str]:
        """Problems with the registry itself, for its authors and the test suite."""
        problems = []
        for item in self.items.values():
            if item.type not in ITEM_TYPES:
                problems.append(f"{item.name}: unknown type {item.type}")
            for dependency in item.registry_dependencies:
                if dependency not in self.items:
                    problems.append(f"{item.name}: depends on unknown item '{dependency}'")
            for path in item.files:
                if not self.remote and not (Path(self.source) / path).is_file():
                    problems.append(f"{item.name}: missing file {path}")
        return problems
