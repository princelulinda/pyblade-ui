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


def test_default_shadows_are_tailwinds_own():
    from pyblade_ui.themes import shadows

    s = shadows()
    assert s["shadow-xs"] == "0 1px 2px 0 color-mix(in oklab, oklch(0 0 0) 5%, transparent)"
    assert s["shadow-sm"] == (
        "0 1px 3px 0 color-mix(in oklab, oklch(0 0 0) 10%, transparent), "
        "0 1px 2px -1px color-mix(in oklab, oklch(0 0 0) 10%, transparent)"
    )
    assert s["shadow-lg"].startswith("0 10px 15px -3px ")
    assert s["shadow-2xl"] == "0 25px 50px -12px color-mix(in oklab, oklch(0 0 0) 25%, transparent)"


def test_shadows_follow_the_base_shadow():
    from pyblade_ui.themes import shadows

    s = shadows({"color": "#635bff", "opacity": 0.2, "blur": 6, "y": 2})
    assert s["shadow-sm"].startswith("0 2px 6px 0 color-mix(in oklab, #635bff 20%, transparent)")
    assert "#635bff 50%" in s["shadow-2xl"]  # 0.2 x 2.5


def test_theme_defines_and_maps_every_shadow():
    from pyblade_ui.themes import SHADOW_TOKENS

    css = render_theme("zinc", "blue")
    for name in SHADOW_TOKENS:
        assert css.count(f"  --{name}: ") == 2  # its value in :root, and its mapping in @theme inline
        assert f"  --{name}: var(--{name});" in css
    assert "color-mix(in oklab, #ff0000 10%" in render_theme(shadow={"color": "#ff0000"})
