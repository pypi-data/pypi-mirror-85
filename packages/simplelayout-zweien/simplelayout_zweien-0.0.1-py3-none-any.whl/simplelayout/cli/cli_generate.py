import argparse


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_grid", type=int, default=10)
    parser.add_argument("--unit_grid", type=int, default=2)
    parser.add_argument("--unit_n", type=int, default=2)
    parser.add_argument("--positions", type=int, nargs="+", default=[1, 4])
    parser.add_argument("-o", "--outdir", type=str, default="example_dir")
    parser.add_argument("--file_name", type=str, default="example")
    options = parser.parse_args()

    if options.board_grid % options.unit_grid:
        raise SystemExit("Error: board_grid 必须整除 unit_grid!")

    if len(options.positions) != options.unit_n:
        raise SystemExit("Error: len(positions) != unit_n!")

    return options
