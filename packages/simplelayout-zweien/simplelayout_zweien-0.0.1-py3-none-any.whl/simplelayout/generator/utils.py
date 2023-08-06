"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    mdict = {"matrix": matrix}
    sio.savemat(file_name + ".mat", mdict)


def save_fig(matrix, file_name):
    plt.imshow(matrix)
    plt.savefig(file_name + ".jpg")


def make_dir(outdir):
    path = Path(outdir).resolve()
    path.mkdir(parents=True, exist_ok=True)
