"""Python data handed to Alpine with `tojson`, and form errors shown by `field` through @error."""

import html
import json
import os
import re

import pytest

from pyblade_ui.utils import tojson_filter


def test_tojson_is_json_and_keeps_unicode():
    assert json.loads(tojson_filter([{"name": "Zoé", "n": 1}])) == [{"name": "Zoé", "n": 1}]


def test_tojson_turns_unknown_values_into_strings():
    import datetime

    assert json.loads(tojson_filter({"d": datetime.date(2026, 10, 13)})) == {"d": "2026-10-13"}


@pytest.fixture(scope="module")
def engine(tmp_path_factory):
    import pyblade_ui  # noqa: F401
    from pyblade import PyBlade
    from pyblade_ui.cli.main import main

    root = tmp_path_factory.mktemp("site")
    (root / "pyblade.toml").write_text('[stack]\nframework = "flask"\n[paths]\ntemplates = "templates"\ncomponents = "components"\n')
    (root / "templates").mkdir()
    main(["--cwd", str(root), "add", "field", "data-table"])
    cwd = os.getcwd()
    os.chdir(root)
    yield PyBlade(dirs=[str(root / "templates")])
    os.chdir(cwd)


def test_rows_reach_alpine_intact(engine):
    rows = [{"id": 1, "name": "O'Brien \"Al\" <b>"}]
    out = engine.render('<pb-ui.data-table :rows="rows" :columns="[]" />', {"rows": rows})
    x_data = html.unescape(re.search(r'x-data="(.*?)"\n', out, re.S).group(1))
    assert json.loads(re.search(r"rows: (\[.*?\]), columns", x_data).group(1)) == rows


@pytest.mark.parametrize("name, error, message", [("email", "true", "Bad email"), ("other", "", "")])
def test_field_shows_the_errors_of_its_name(engine, name, error, message):
    template = (
        f'<pb-ui.field :errors="errors" name="{name}">'
        f'<pb-ui.field-error :errors="errors" name="{name}" /></pb-ui.field>'
    )
    out = engine.render(template, {"errors": {"email": ["Bad email"]}})
    assert f'data-error="{error}"' in out
    assert re.search(r'data-slot="field-error"[^>]*>([^<]*)</p>', out).group(1) == message
