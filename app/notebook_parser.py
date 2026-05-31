import nbformat


def extract_code_from_notebook(file_path: str) -> str:
    notebook = nbformat.read(file_path, as_version=4)

    code_cells = []

    for cell in notebook.cells:
        if cell.cell_type == "code":
            code_cells.append(cell.source)

    return "\n\n".join(code_cells)