"""Template rendering for commit messages."""

BUILTIN_TEMPLATES = {
    "default": "{tag}: {count} files ({files})",
    "simple": "{tag}: {count} files",
    "short": "{tag}: {files}",
}


def render_template(template: str, *, tag: str, files: str, count: int) -> str:
    """Render a commit message from a built-in template name or a custom format string.

    ``template`` is either a known built-in name (``default``/``simple``/``short``)
    or a raw ``str.format`` template using ``{tag}``, ``{files}``, ``{count}``.
    """
    fmt = BUILTIN_TEMPLATES.get(template, template)
    try:
        return fmt.format(tag=tag, files=files, count=count)
    except (KeyError, IndexError, ValueError):
        # Unknown placeholder in a custom template — fall back to a safe default.
        return f"{tag}: {count} files"
