"""Check a registry folder before publishing it: every file exists, every dependency is known,
and every component has the single root node PyBlade requires.

    python scripts/check_registry.py [path/to/registry]
"""

import sys

from pyblade.utils import validate_single_root_node

from pyblade_ui.registry import Registry


def main() -> int:
    registry = Registry(sys.argv[1] if len(sys.argv) > 1 else "")
    problems = registry.validate()
    for item in registry.items.values():
        for path in item.files:
            if path.endswith(".html") and not validate_single_root_node(registry.read_file(path)):
                problems.append(f"{item.name}: {path} has more than one root node")
    for problem in problems:
        print(f"✘ {problem}")
    if not problems:
        print(f"✔ {len(registry.items)} items, registry OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
