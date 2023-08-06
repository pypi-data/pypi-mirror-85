"""
数据生成的主要逻辑
"""


import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:
    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        布局矩阵
    """
    matrix = np.zeros(shape=(board_grid, board_grid))
    units_per_row = int(board_grid / unit_grid)
    for pos in positions:
        row, col = get_row_col(pos, units_per_row)
        idx_row = slice(row * unit_grid, (row + 1) * unit_grid)
        idx_col = slice(col * unit_grid, (col + 1) * unit_grid)
        matrix[idx_row, idx_col] = 1

    return matrix


def get_row_col(pos: int, units_per_row: int) -> tuple:
    """计算行、列位置

    Args:
        pos (int): 1 <= pos <= units_per_row^2
        units_per_row (int): 每行可放置组件的位置数

    Returns:
        tuple: row, col, 从 0 开始
    """
    pos_ = pos - 1
    row = int(pos_ / units_per_row)
    col = int(pos_ % units_per_row)
    return row, col
