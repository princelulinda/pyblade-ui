"""The sidebar's server side: its state is read from a cookie and rendered before any JavaScript runs."""

from types import SimpleNamespace

import pytest

from pyblade_ui import sidebar_open
from pyblade_ui.context_processors import sidebar


@pytest.mark.parametrize(
    "request_, expected",
    [
        (SimpleNamespace(COOKIES={"sidebar_state": "false"}), False),  # Django
        (SimpleNamespace(COOKIES={"sidebar_state": "true"}), True),
        (SimpleNamespace(cookies={"sidebar_state": "false"}), False),  # Flask, Starlette, FastAPI...
        (SimpleNamespace(cookies={}), True),
        (SimpleNamespace(), True),
    ],
)
def test_sidebar_open_reads_the_cookie(request_, expected):
    assert sidebar_open(request_) is expected


def test_default_without_cookie():
    assert sidebar_open(SimpleNamespace(cookies={}), default=False) is False


def test_django_context_processor():
    assert sidebar(SimpleNamespace(COOKIES={"sidebar_state": "false"})) == {"sidebar_open": False}


@pytest.fixture(scope="module")
def engine(tmp_path_factory):
    import os
    import sys

    from pyblade import PyBlade
    from pyblade_ui.cli.main import main

    root = tmp_path_factory.mktemp("site")
    (root / "pyblade.toml").write_text('[stack]\nframework = "flask"\n[paths]\ntemplates = "templates"\ncomponents = "components"\n')
    (root / "templates").mkdir()
    main(["--cwd", str(root), "add", "sidebar-layout"])
    cwd = os.getcwd()
    os.chdir(root)
    yield PyBlade(dirs=[str(root / "templates")])
    os.chdir(cwd)


@pytest.mark.parametrize("open_, state, collapsible", [(True, "expanded", ""), (False, "collapsed", "icon")])
def test_state_is_rendered_on_the_server(engine, open_, state, collapsible):
    import pyblade_ui  # noqa: F401

    html = engine.render('<pb-blocks.sidebar-layout :open="sidebar_open">x</pb-blocks.sidebar-layout>', {"sidebar_open": open_})
    assert f'data-state="{state}"' in html
    assert f'data-collapsible="{collapsible}"' in html
    assert f"open: {str(open_).lower()}," in html
