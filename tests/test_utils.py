import pytest

from pyblade_ui.utils import tw_merge


@pytest.mark.parametrize(
    "classes, expected",
    [
        (["px-4 py-2", "px-8"], "py-2 px-8"),
        (["px-4 py-2", "p-0"], "p-0"),
        (["p-4", "px-2"], "p-4 px-2"),
        (["bg-primary text-white", "bg-red-500"], "text-white bg-red-500"),
        (["text-sm text-muted-foreground", "text-lg"], "text-muted-foreground text-lg"),
        (["text-sm text-muted-foreground", "text-red-500"], "text-sm text-red-500"),
        (["inline-flex h-9", "hidden"], "h-9 hidden"),
        (["hover:bg-accent bg-background", "hover:bg-red-500"], "bg-background hover:bg-red-500"),
        (["rounded-md", "rounded-full"], "rounded-full"),
        (["border border-input", "border-red-500"], "border border-red-500"),
        (["md:px-4", "px-2"], "md:px-4 px-2"),
        (["size-9", "w-full"], "size-9 w-full"),
        (["w-4 h-4", "size-9"], "size-9"),
        (["flex flex-col", "flex-row"], "flex flex-row"),
        (["a b", None, "", "b c"], "a b c"),
    ],
)
def test_tw_merge(classes, expected):
    assert tw_merge(*classes) == expected
