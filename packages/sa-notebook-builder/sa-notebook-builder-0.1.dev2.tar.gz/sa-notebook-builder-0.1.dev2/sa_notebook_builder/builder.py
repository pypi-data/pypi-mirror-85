import nbformat as nbf


class Builder:
    def __init__(self):
        self._inport_cells = []
        self._cells = []

    def render(self, filename: str):
        nb = nbf.v4.new_notebook()
        nb["cells"] = self._inport_cells + self._cells
        nbf.write(nb, filename)

    def add_markdown(self, markdown: str):
        cell = nbf.v4.new_markdown_cell(markdown)
        self._cells.append(cell)


if __name__ == '__main__':
    b = Builder()
    b.add_markdown("## Complex z")
    b.render('main.ipynb')
