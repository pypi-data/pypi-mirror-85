import click
from click._compat import term_len
from click.formatting import iter_rows, measure_table, wrap_text


class SeparateHelpFormatter(click.HelpFormatter):
    """This class provides splitting HelpFormatter."""

    def __init__(self, max_width=100, *args, **kwargs):
        super().__init__(max_width=max_width, *args, **kwargs)

    def write_dl(self, rows, col_max=30, col_spacing=2):  # noqa: D102
        rows = list(rows)
        widths = measure_table(rows)
        if len(widths) != 2:
            raise TypeError("Expected two columns for definition list")

        first_col = min(widths[0], col_max) + col_spacing

        for first, second in iter_rows(rows, len(widths)):
            self.write(f"{'':>{self.current_indent}}{first}")
            if not second:
                self.write("\n")
                continue
            if term_len(first) <= first_col - col_spacing:
                self.write(" " * (first_col - term_len(first)))
            else:
                self.write("\n")
                self.write(" " * (first_col + self.current_indent))

            text_width = max(self.width - first_col - 2, 10)
            wrapped_text = wrap_text(second, text_width, preserve_paragraphs=True)
            lines = wrapped_text.splitlines()

            if lines:
                self.write(f"{lines[0]}\n")

                for line in lines[1:]:
                    self.write(f"{'':>{first_col + self.current_indent}}{line}\n")
            else:
                self.write("\n")
