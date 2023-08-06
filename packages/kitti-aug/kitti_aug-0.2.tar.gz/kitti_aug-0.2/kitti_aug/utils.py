# many methods are imported from https://github.com/kuixu/kitti_object_vis

import os
import numpy as np
import random
import math


def roty(t):
    ''' Rotation about the y-axis. '''
    c = np.cos(t)
    s = np.sin(t)
    return np.array([[c,  0,  s],
                     [0,  1,  0],
                     [-s, 0,  c]])

def project_to_image(pts_3d, P):
    n = pts_3d.shape[0]
    pts_3d_extend = np.hstack((pts_3d, np.ones((n,1))))
    #print(('pts_3d_extend shape: ', pts_3d_extend.shape))
    pts_2d = np.dot(pts_3d_extend, np.transpose(P)) # nx3
    pts_2d[:,0] /= pts_2d[:,2]
    pts_2d[:,1] /= pts_2d[:,2]
    return pts_2d[:,0:2]

def inverse_rigid_trans(Tr):
    ''' Inverse a rigid body transform matrix (3x4 as [R|t])
        [R'|-R't; 0|1]
    '''
    inv_Tr = np.zeros_like(Tr) # 3x4
    inv_Tr[0:3,0:3] = np.transpose(Tr[0:3,0:3])
    inv_Tr[0:3,3] = np.dot(-np.transpose(Tr[0:3,0:3]), Tr[0:3,3])
    return inv_Tr

def cart2hom(pts_3d):
        ''' Input: nx3 points in Cartesian
            Oupput: nx4 points in Homogeneous by pending 1
        '''
        n = pts_3d.shape[0]
        pts_3d_hom = np.hstack((pts_3d, np.ones((n,1))))
        return pts_3d_hom
def project_ref_to_velo(pts_3d_ref, Tr_velo_to_cam):
        pts_3d_ref = cart2hom(pts_3d_ref) # nx4
        C2V = inverse_rigid_trans(Tr_velo_to_cam.reshape((3, 4)))
        return np.dot(pts_3d_ref, np.transpose(C2V))

def project_rect_to_ref(pts_3d_rect, R0_rect):
        ''' Input and Output are nx3 points '''
        return np.transpose(np.dot(np.linalg.inv(R0_rect.reshape((3, 3))), np.transpose(pts_3d_rect)))


def project_point_from_camera_coor_to_velo_coor(location, dimemsion, agnle, calib_data):
    R = roty(agnle)
    h, w, l = dimemsion
    x, y, z = location
    x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2];
    y_corners = [0,0,0,0,-h,-h,-h,-h];
    z_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2];
    
    # rotate and translate 3d bounding box
    corners_3d = np.dot(R, np.vstack([x_corners,y_corners,z_corners]))
    #print corners_3d.shape
    corners_3d[0,:] = corners_3d[0,:] + x;
    corners_3d[1,:] = corners_3d[1,:] + y;
    corners_3d[2,:] = corners_3d[2,:] + z;
    #print 'cornsers_3d: ', corners_3d
    # only draw 3d bounding box for objs in front of the camera
#     if np.any(corners_3d[2,:]<0.1):
#         corners_2d = None
#         return corners_2d, np.transpose(corners_3d)

    # project the 3d bounding box into the image plane
#     corners_2d = project_to_image(np.transpose(corners_3d), calib_data['P3'].reshape((3, 4)));
    box3d_pts_3d = np.transpose(corners_3d)

    pts_3d_ref = project_rect_to_ref(box3d_pts_3d, calib_data['R0_rect'])
    result = project_ref_to_velo(pts_3d_ref, calib_data['Tr_velo_to_cam'])
#     print(result)
    return result
