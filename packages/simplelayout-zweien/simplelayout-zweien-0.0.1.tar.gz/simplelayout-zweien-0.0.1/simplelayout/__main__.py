from simplelayout.cli.cli_generate import get_options
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix, save_fig, make_dir
from pathlib import Path

def main():
    options = get_options()
    matrix = generate_matrix(
        board_grid=options.board_grid,
        unit_grid=options.unit_grid,
        unit_n=options.unit_n,
        positions=options.positions,
    )
    make_dir(options.outdir)
    path = Path(options.outdir) / options.file_name
    save_matrix(matrix, file_name=str(path))
    save_fig(matrix, file_name=str(path))


if __name__ == "__main__":
    main()
