import pytest

from pyblade_ui.themes import BASES, COLORS, CUSTOM_MARKER, TOKENS, custom_part, render_theme


@pytest.mark.parametrize("base", BASES)
@pytest.mark.parametrize("color", COLORS)
def test_every_theme_defines_every_token(base, color):
    css = render_theme(base, color)
    for token in TOKENS:
        assert css.count(f"  --{token}:") == 2  # :root and .dark
        assert f"--color-{token}: var(--{token});" in css


def test_custom_part_survives_regeneration():
    first = render_theme("zinc", "blue") + ":root { --primary: hotpink; }\n"
    second = render_theme("slate", "rose", custom=custom_part(first))
    assert "base=slate color=rose" in second
    assert second.endswith(CUSTOM_MARKER + "\n:root { --primary: hotpink; }\n")


def test_unknown_base():
    with pytest.raises(ValueError):
        render_theme("purple")
