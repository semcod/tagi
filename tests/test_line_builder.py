"""Tests for the shared line accumulator."""

from tagi.utils.line_builder import LineBuilder


class TestLineBuilder:
    def test_add_single_line(self):
        builder = LineBuilder()
        builder.add("first")
        assert builder.as_list() == ["first"]

    def test_add_multiple_lines(self):
        builder = LineBuilder()
        builder.add("a", "b")
        builder.add("c")
        assert builder.as_list() == ["a", "b", "c"]

    def test_add_blank_line(self):
        builder = LineBuilder()
        builder.add("a", "", "b")
        assert builder.text() == "a\n\nb"

    def test_empty_builder_renders_empty_string(self):
        assert LineBuilder().text() == ""
        assert LineBuilder().as_list() == []
