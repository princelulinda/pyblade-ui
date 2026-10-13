from pyblade_ui.registry import Registry


def test_bundled_registry_is_valid():
    assert Registry().validate() == []


def test_resolve_puts_dependencies_first():
    names = [item.name for item in Registry().resolve(["login-form"])]
    assert names.index("card") < names.index("login-form")
    assert names.index("button") < names.index("login-form")
    assert len(names) == len(set(names))


def test_every_component_has_a_single_root_node():
    from pyblade.utils import validate_single_root_node

    registry = Registry()
    for item in registry.items.values():
        for path in item.files:
            assert validate_single_root_node(registry.read_file(path)), path
