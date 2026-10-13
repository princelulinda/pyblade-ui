"""Install every component into a fresh PyBlade project and render its usage example."""

import re

import pytest

from pyblade_ui.cli.main import main
from pyblade_ui.registry import Registry


@pytest.fixture(scope="module")
def project(tmp_path_factory):
    root = tmp_path_factory.mktemp("site")
    (root / "pyblade.toml").write_text(
        '[stack]\nframework = "flask"\n[paths]\ntemplates = "templates"\ncomponents = "components"\n'
    )
    (root / "templates").mkdir()
    assert main(["--cwd", str(root), "init", "--base", "zinc", "--color", "blue"]) == 0
    assert main(["--cwd", str(root), "add", "--all"]) == 0
    return root


def test_init_writes_config_theme_and_stylesheet(project):
    assert 'base = "zinc"' in (project / "pyblade-ui.toml").read_text()
    assert "--primary: oklch(0.546 0.245 262.881);" in (project / "static/css/theme.css").read_text()
    tailwind = (project / "static/css/tailwind.css").read_text()
    assert tailwind.splitlines()[:2] == ['@import "tailwindcss";', '@import "./theme.css";']


def test_add_copies_files(project):
    assert (project / "components/ui/button.html").is_file()
    assert (project / "components/blocks/login_form.html").is_file()


def test_add_keeps_local_changes(project, capsys):
    button = project / "components/ui/button.html"
    original = button.read_text()
    button.write_text(original + "\n{# mine #}")
    main(["--cwd", str(project), "add", "button"])
    assert button.read_text().endswith("{# mine #}")
    main(["--cwd", str(project), "diff", "button"])
    assert "+{# mine #}" in capsys.readouterr().out
    button.write_text(original)


def test_theme_set(project):
    assert main(["--cwd", str(project), "theme", "set", "--color", "rose", "--radius", "1rem"]) == 0
    css = (project / "static/css/theme.css").read_text()
    assert "--radius: 1rem;" in css and "oklch(0.586 0.253 17.585)" in css


CONTEXT = {
    "user": {"photo_url": "/me.png", "name": "Ada"},
    "users": [{"name": "Ada"}, {"name": "Grace"}],
    "sidebar_open": True,  # what pyblade_ui.sidebar_open(request) gives
    "form": {"errors": {"email": ["Enter a valid email address."]}},
    "article": {"html": "<p>Hello</p>"},
}


@pytest.mark.parametrize("name", list(Registry().items))
def test_usage_renders(project, monkeypatch, name):
    import pyblade_ui  # noqa: F401 -- registers the cn filter
    from pyblade import PyBlade

    monkeypatch.chdir(project)
    usage = Registry().get(name).usage
    html = PyBlade(dirs=[str(project / "templates")]).render(usage, dict(CONTEXT))

    assert "<pb-" not in html, html
    assert "Traceback" not in html and "TemplateRenderError" not in html, html
    # One class attribute per tag: the caller's classes are merged, never duplicated
    for tag in re.findall(r"<[a-z][^>]*>", html):
        assert tag.count(' class="') <= 1, tag


def test_caller_class_and_attributes_are_merged(project, monkeypatch):
    import pyblade_ui  # noqa: F401
    from pyblade import PyBlade

    monkeypatch.chdir(project)
    html = PyBlade().render('<pb-ui.button variant="outline" class="w-full px-8" id="go" disabled>Go</pb-ui.button>', {})
    assert 'id="go"' in html and " disabled" in html
    classes = re.search(r' class="([^"]*)"', html).group(1).split()
    assert "w-full" in classes and "px-8" in classes and "px-4" not in classes
    assert "bg-background" in classes  # outline variant
