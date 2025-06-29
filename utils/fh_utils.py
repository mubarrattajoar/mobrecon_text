from __future__ import print_function, unicode_literals
import numpy as np
import json
import os
import time
import skimage.io as io
from utils.read import read_mesh as read_mesh_


""" General util functions. """
def _assert_exist(p):
    msg = 'File does not exists: %s' % p
    assert os.path.exists(p), msg


def json_load(p):
    _assert_exist(p)
    with open(p, 'r') as fi:
        d = json.load(fi)
    return d

def projectPoints(xyz, K):
    """ Project 3D coordinates into image space. """
    xyz = np.array(xyz)
    K = np.array(K)
    uv = np.matmul(K, xyz.T).T
    return uv[:, :2] / uv[:, -1:]


""" Draw functions. """
def plot_hand(axis, coords_hw, vis=None, color_fixed=None, linewidth='1', order='hw', draw_kp=True):
    """ Plots a hand stick figure into a matplotlib figure. """
    if order == 'uv':
        coords_hw = coords_hw[:, ::-1]

    colors = np.array([[0.4, 0.4, 0.4],
                       [0.4, 0.0, 0.0],
                       [0.6, 0.0, 0.0],
                       [0.8, 0.0, 0.0],
                       [1.0, 0.0, 0.0],
                       [0.4, 0.4, 0.0],
                       [0.6, 0.6, 0.0],
                       [0.8, 0.8, 0.0],
                       [1.0, 1.0, 0.0],
                       [0.0, 0.4, 0.2],
                       [0.0, 0.6, 0.3],
                       [0.0, 0.8, 0.4],
                       [0.0, 1.0, 0.5],
                       [0.0, 0.2, 0.4],
                       [0.0, 0.3, 0.6],
                       [0.0, 0.4, 0.8],
                       [0.0, 0.5, 1.0],
                       [0.4, 0.0, 0.4],
                       [0.6, 0.0, 0.6],
                       [0.7, 0.0, 0.8],
                       [1.0, 0.0, 1.0]])

    colors = colors[:, ::-1]

    # define connections and colors of the bones
    if coords_hw.shape[0] == 21:
        bones = [((0, 1), colors[1, :]),
                 ((1, 2), colors[2, :]),
                 ((2, 3), colors[3, :]),
                 ((3, 4), colors[4, :]),

                 ((0, 5), colors[5, :]),
                 ((5, 6), colors[6, :]),
                 ((6, 7), colors[7, :]),
                 ((7, 8), colors[8, :]),

                 ((0, 9), colors[9, :]),
                 ((9, 10), colors[10, :]),
                 ((10, 11), colors[11, :]),
                 ((11, 12), colors[12, :]),

                 ((0, 13), colors[13, :]),
                 ((13, 14), colors[14, :]),
                 ((14, 15), colors[15, :]),
                 ((15, 16), colors[16, :]),

                 ((0, 17), colors[17, :]),
                 ((17, 18), colors[18, :]),
                 ((18, 19), colors[19, :]),
                 ((19, 20), colors[20, :])]
    else:
        bones = [((0, 1), colors[1, :]),
                 ((1, 2), colors[2, :]),
                 ((2, 3), colors[3, :]),

                 ((0, 4), colors[5, :]),
                 ((4, 5), colors[6, :]),
                 ((5, 6), colors[7, :]),

                 ((0, 7), colors[9, :]),
                 ((7, 8), colors[10, :]),
                 ((8, 9), colors[11, :]),
                 ((9, 10), colors[12, :]),

                 ((8, 11), colors[13, :]),
                 ((11, 12), colors[14, :]),
                 ((12, 13), colors[15, :]),

                 ((8, 14), colors[17, :]),
                 ((14, 15), colors[18, :]),
                 ((15, 16), colors[19, :])]

    if vis is None:
        vis = np.ones_like(coords_hw[:, 0]) == 1.0

    for connection, color in bones:
        if (vis[connection[0]] == False) or (vis[connection[1]] == False):
            continue

        coord1 = coords_hw[connection[0], :]
        coord2 = coords_hw[connection[1], :]
        coords = np.stack([coord1, coord2])
        if color_fixed is None:
            axis.plot(coords[:, 1], coords[:, 0], color=color, linewidth=linewidth)
        else:
            axis.plot(coords[:, 1], coords[:, 0], color_fixed, linewidth=linewidth)

    if not draw_kp:
        return

    for i in range(coords_hw.shape[0]):
        if vis[i] > 0.5:
            axis.plot(coords_hw[i, 1], coords_hw[i, 0], 'o', color=colors[i, :])


""" Dataset related functions. """
def db_size(set_name):
    """ Hardcoded size of the datasets. """
    if set_name == 'training':
        return 32560  # number of unique samples (they exists in multiple 'versions')
    elif set_name == 'evaluation':
        return 3960
    else:
        assert 0, 'Invalid choice.'


def load_db_annotation(base_path, writer=None, set_name=None):
    if set_name in ['training', 'train']:
        if writer is not None:
            writer.print_str('Loading FreiHAND training set index ...')
        t = time.time()
        k_path = os.path.join(base_path, '%s_K.json' % 'training')

        # assumed paths to data containers
        mano_path = os.path.join(base_path, '%s_mano.json' % 'training')
        xyz_path = os.path.join(base_path, '%s_xyz.json' % 'training')

        # load if exist
        K_list = json_load(k_path)
        mano_list = json_load(mano_path)
        xyz_list = json_load(xyz_path)

        # should have all the same length
        assert len(K_list) == len(mano_list), 'Size mismatch.'
        assert len(K_list) == len(xyz_list), 'Size mismatch.'
        if writer is not None:
            writer.print_str('Loading of %d %s samples done in %.2f seconds' % (len(K_list), set_name, time.time()-t))
        return zip(K_list, mano_list, xyz_list)
    elif set_name in ['evaluation', 'eval', 'val']:
        if writer is not None:
            writer.print_str('Loading FreiHAND training set index ...')
        t = time.time()
        k_path = os.path.join(base_path, '%s_K.json' % 'val')

        # assumed paths to data containers
        mano_path = os.path.join(base_path, '%s_mano.json' % 'val')
        xyz_path = os.path.join(base_path, '%s_xyz.json' % 'val')

        # load if exist
        K_list = json_load(k_path)
        mano_list = json_load(mano_path)
        xyz_list = json_load(xyz_path)

        # should have all the same length
        assert len(K_list) == len(mano_list), 'Size mismatch.'
        assert len(K_list) == len(xyz_list), 'Size mismatch.'
        if writer is not None:
            writer.print_str('Loading of %d %s samples done in %.2f seconds' % (len(K_list), set_name, time.time() - t))
        return zip(K_list, mano_list, xyz_list)
    elif set_name in ['test']:
        if writer is not None:
            writer.print_str('Loading FreiHAND eval set index ...')
        t = time.time()
        k_path = os.path.join(base_path, '%s_K.json' % 'evaluation')
        scale_path = os.path.join(base_path, '%s_scale.json' % 'evaluation')
        K_list = json_load(k_path)
        scale_list = json_load(scale_path)

        assert len(K_list) == len(scale_list), 'Size mismatch.'
        if writer is not None:
            writer.print_str('Loading of %d eval samples done in %.2f seconds' % (len(K_list), time.time() - t))
        return zip(K_list, scale_list)
    else:
        raise Exception('set_name error: ' + set_name)


class sample_version:
    gs = 'gs'  # green screen
    hom = 'hom'  # homogenized
    sample = 'sample'  # auto colorization with sample points
    auto = 'auto'  # auto colorization without sample points: automatic color hallucination

    db_size = db_size('training')

    @classmethod
    def valid_options(cls):
        return [cls.gs, cls.hom, cls.sample, cls.auto]


    @classmethod
    def check_valid(cls, version):
        msg = 'Invalid choice: "%s" (must be in %s)' % (version, cls.valid_options())
        assert version in cls.valid_options(), msg

    @classmethod
    def map_id(cls, id, version):
        cls.check_valid(version)
        return id + cls.db_size*cls.valid_options().index(version)


def read_img(idx, base_path, set_name, version=None):
    if version is None:
        version = sample_version.gs

    if set_name == 'evaluation':
        assert version == sample_version.gs, 'This the only valid choice for samples from the evaluation split.'

    img_rgb_path = os.path.join(base_path, set_name, 'rgb', '%08d.jpg' % sample_version.map_id(idx, version))
    if not os.path.exists(img_rgb_path):
        img_rgb_path = os.path.join(base_path, set_name, 'rgb2', '%08d.jpg' % idx)

    _assert_exist(img_rgb_path)
    return io.imread(img_rgb_path)


def read_img_abs(idx, base_path, set_name):
    img_rgb_path = os.path.join(base_path, set_name, 'rgb', '%08d.jpg' % idx)
    if not os.path.exists(img_rgb_path):
        img_rgb_path = os.path.join(base_path, set_name, 'rgb2', '%08d.jpg' % idx)

    _assert_exist(img_rgb_path)
    return io.imread(img_rgb_path)


def read_msk(idx, base_path, set_name):
    mask_path = os.path.join(base_path, set_name, 'mask',
                             '%08d.jpg' % idx)
    _assert_exist(mask_path)
    return (io.imread(mask_path)[:, :, 0] > 240).astype(np.uint8)


def read_mask_woclip(idx, base_path, set_name):
    mask_path = os.path.join(base_path, set_name, 'mask',
                             '%08d.jpg' % idx)
    _assert_exist(mask_path)
    return io.imread(mask_path)[:, :, 0]

#edited by mub
def read_mesh(idx, base_path,set_name):
    mesh_path = os.path.join(base_path, set_name, 'mesh',
                             '%08d.ply' % idx)
    _assert_exist(mesh_path)
    return read_mesh_(mesh_path)

