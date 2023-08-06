from .utils import *
from .fv_utils import *
import os
import math
import numpy as np

class LabelReader:

    def __init__(self, label_path, calib_path, rot, tr, sc, ang, calib_reader,
                    x_range=(0, 70), 
                    y_range=(-40, 40), 
                    z_range=(-2.5, 1), 
                    size=(448, 512, 35), 
                    get_actual_dims=False, 
                    from_file=True, fliplr=False):
        self.label_path = label_path
        self.calib_path = calib_path
        self.rot = rot
        self.tr = tr
        self.sc = sc
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.size = size
        self.get_actual_dims = get_actual_dims
        self.from_file = from_file
        self.ang = ang
        self.calib_reader = calib_reader
        self.fliplr = fliplr


    def read_label(self):

        """
        the file format is as follows: 
        type, truncated, occluded, alpha, bbox_left, bbox_top, bbox_right, bbox_bottom,
        dimensions_height, dimensions_width, dimensions_length, location_x, location_y, location_z,
        rotation_y, score) 
        """
        if self.from_file:
            lines = []
            with open(self.label_path) as label_file:
                lines = label_file.readlines()
        else:
            lines = self.label_path.split('\n')

        # filter car class
        lines = list(map(lambda x: x.split(), lines))
        if len(lines) > 0:
           lines = list(filter(lambda x: len(x) > 0 and ( x[0] in ['Car']), lines))
        
        def get_parameter(index):
            return list(map(lambda x: x[index], lines))
        
        classes = np.array(get_parameter(0))
        dimension_height = np.array(get_parameter(8)).astype(float)
        dimension_width = np.array(get_parameter(9)).astype(float)
        dimension_length = np.array(get_parameter(10)).astype(float)
        location_x = np.array(get_parameter(11)).astype(float)
        location_y = np.array(get_parameter(12)).astype(float)
        location_z = np.array(get_parameter(13)).astype(float)
        angles = np.array(get_parameter(14)).astype(float)
        
        calib_data = self.calib_reader.read_calib()

        locations = np.array([[location_x[i], location_y[i], location_z[i]] for i in range(len(classes))])

        if len(locations) > 0 and len(locations[0]) > 0:
            locations = self.project_rect_to_velo2(self.rot, self.tr, self.sc, locations, calib_data['R0_rect'].reshape((3, 3)), calib_data['Tr_velo_to_cam'].reshape((3, 4)))
       

        indx = []
        i = 0
        for point in locations:
            if (point[0] >= self.x_range[0]  and point[0] <= self.x_range[1])\
                and (point[1] >= self.y_range[0] and point[1] <= self.y_range[1])\
                and (point[2] >= self.z_range[0] and point[2] <= self.z_range[1]):
                indx.append(i)
            i += 1

        
        locations = np.array(list(filter(lambda point: (point[0] >= self.x_range[0]  and point[0] <= self.x_range[1])
                                        and (point[1] >= self.y_range[0] and point[1] <= self.y_range[1])
                                        and (point[2] >= self.z_range[0] and point[2] <= self.z_range[1]) , locations)))
        
        if len(indx) > 0:
            dimension_height = dimension_height[indx]
            dimension_width = dimension_width[indx]
            dimension_length = dimension_length[indx]
            location_x = location_x[indx]
            location_y = location_y[indx]
            location_z = location_z[indx]
            angles = angles[indx]
            classes = classes[indx]

        points = []
        sl = []
        sw = []
        sh = []
        for i in range(len(locations)):
            temp = self.project_point_from_camera_coor_to_velo_coor2(self.rot, self.tr, self.sc, [location_x[i], location_y[i], location_z[i]], 
                                                            [dimension_height[i], dimension_width[i], dimension_length[i]],
                                                            angles[i],
                                                            calib_data)
                    
        
        
            points.append(temp[0])
            sl.append(temp[1])
            sw.append(temp[2])
            sh.append(temp[3])
        
        x_size = (self.x_range[1] - self.x_range[0])
        y_size = (self.y_range[1] - self.y_range[0])
        z_size = (self.z_range[1] - self.z_range[0])
                
        x_fac = (self.size[0]-1) / x_size
        y_fac = (self.size[1]-1) / y_size
        z_fac = (self.size[2]-1) / z_size

        if self.get_actual_dims:
            import math
            for i in range(len(points)):
                b = points[i]
                x0 = b[0][0]
                y0 = b[0][1]
                x1 = b[1][0]
                y1 = b[1][1]
                x2 = b[2][0]
                y2 = b[2][1]
                u0 = -(x0) * x_fac + self.size[0]
                v0 = -(y0 + self.size[2]) * y_fac + self.size[1]
                u1 = -(x1) * x_fac + self.size[0]
                v1 = -(y1 + self.size[2]) * y_fac + self.size[1]
                u2 = -(x2) * x_fac + self.size[0]
                v2 = -(y2 + self.size[2]) * y_fac + self.size[1]
                dimension_length[i] = math.sqrt((v1-v2)**2 + (u1-u2)**2)
                dimension_width[i] = math.sqrt((v1-v0)**2 + (u1-u0)**2)
                dimension_height[i] = math.sqrt((-(b[0][2]+(-1*self.z_range[1]))*z_fac-(-b[4][2]+self.z_range[1])*z_fac)**2)

        
        # for i in range(len(locations)):
        #     if angles[i] < 0:
        #         angles[i] += np.pi
        if self.get_actual_dims:
            output = [[-(locations[i][0] + -1*self.x_range[0]) * x_fac + self.size[0], -(locations[i][1] + -1*self.y_range[0]) * y_fac + self.size[1], -(locations[i][2] + -1*self.z_range[0]) * z_fac + self.size[2], 
                    dimension_length[i], dimension_width[i], dimension_height[i], angles[i]] 
                    for i in range(len(locations))]
        else:
            output = [[-(locations[i][0] + -1*self.x_range[0]) * x_fac + self.size[0], -(locations[i][1] + -1*self.y_range[0]) * y_fac + self.size[1], -(locations[i][2] + -1*self.z_range[0]) * z_fac + self.size[2], 
                    dimension_length[i]*sl[i], dimension_width[i]*sw[i], dimension_height[i]*sh[i], angles[i]] 
                    for i in range(len(locations))]
       

        if self.ang != 0:
            for i in range(len(locations)):
              output[i][6] = output[i][6] - self.ang / (180/np.pi)
              if output[i][6] < -np.pi:
                  output[i][6] = output[i][6] + 2 * np.pi
              if output[i][6] > np.pi:
                  output[i][6] = output[i][6] - 2 * np.pi


        if self.fliplr:
            for i in range(len(locations)):
                h = self.size[1]
                output[i][1] = h - output[i][1]
                output[i][6] = ((-output[i][6]*(180/np.pi)) + 180) / (180/np.pi)
                if output[i][6] < -np.pi:
                  output[i][6] = output[i][6] + 2 * np.pi
                if output[i][6] > np.pi:
                  output[i][6] = output[i][6] - 2 * np.pi

        output = list(filter(lambda point: 0 <= point[0] < self.size[0] and 0 <= point[1] < self.size[1] and 0 <= point[2] < self.size[2] , output))
        output = np.array(output)

        return points, output


    def project_rect_to_velo2(self, rot, tr, sc, pts_3d_rect, RO, Tr_velo_to_cam):
        ''' Input: nx3 points in rect camera coord.
            Output: nx3 points in velodyne coord.
        ''' 
        pts_3d_ref = self.project_rect_to_ref(pts_3d_rect, RO)
        temp = self.project_ref_to_velo(pts_3d_ref, Tr_velo_to_cam)
        temp = temp.transpose() + tr[:3, :1]
        temp = np.dot(sc[:3, :3], np.dot(rot[:3, :3], temp)).transpose()
        return temp

    def project_rect_to_ref(self, pts_3d_rect, R0):
        ''' Input and Output are nx3 points '''
        return np.transpose(np.dot(np.linalg.inv(R0.reshape((3, 3))), np.transpose(pts_3d_rect)))
    
    def project_ref_to_velo(self, pts_3d_ref, Tr_velo_to_cam):
        pts_3d_ref = self.cart2hom(pts_3d_ref) # nx4
        C2V = self.inverse_rigid_trans(Tr_velo_to_cam.reshape((3, 4)))
        return np.dot(pts_3d_ref, np.transpose(C2V))

    def cart2hom(self, pts_3d):
        ''' Input: nx3 points in Cartesian
            Oupput: nx4 points in Homogeneous by pending 1
        '''
        n = pts_3d.shape[0]
        pts_3d_hom = np.hstack((pts_3d, np.ones((n,1))))
        return pts_3d_hom

    def inverse_rigid_trans(self, Tr):
        ''' Inverse a rigid body transform matrix (3x4 as [R|t])
            [R'|-R't; 0|1]
        '''
        inv_Tr = np.zeros_like(Tr) # 3x4
        inv_Tr[0:3,0:3] = np.transpose(Tr[0:3,0:3])
        inv_Tr[0:3,3] = np.dot(-np.transpose(Tr[0:3,0:3]), Tr[0:3,3])
        return inv_Tr


    def project_point_from_camera_coor_to_velo_coor2(self, rot, tr, sc, location, dimemsion, agnle, calib_data):
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

        box3d_pts_3d = np.transpose(corners_3d)

        pts_3d_ref = project_rect_to_ref(box3d_pts_3d, calib_data['R0_rect'])
        result = project_ref_to_velo(pts_3d_ref, calib_data['Tr_velo_to_cam'])
        
        temp = result
        
        
        x_size = (self.x_range[1] - self.x_range[0])
        y_size = (self.y_range[1] - self.y_range[0])
        z_size = (self.z_range[1] - self.z_range[0])
                
        x_fac = (self.size[0]-1) / x_size
        y_fac = (self.size[1]-1) / y_size
        z_fac = (self.size[2]-1) / z_size
        
        b = temp
        x0 = b[0][0]
        y0 = b[0][1]
        x1 = b[1][0]
        y1 = b[1][1]
        x2 = b[2][0]
        y2 = b[2][1]
        u0 = -(x0) * x_fac + self.size[0]
        v0 = -(y0 + self.size[2]) * y_fac + self.size[1]
        u1 = -(x1) * x_fac + self.size[0]
        v1 = -(y1 + self.size[2]) * y_fac + self.size[1]
        u2 = -(x2) * x_fac + self.size[0]
        v2 = -(y2 + self.size[2]) * y_fac + self.size[1]
        dimension_length = math.sqrt((v1-v2)**2 + (u1-u2)**2)
        dimension_width = math.sqrt((v1-v0)**2 + (u1-u0)**2)
        dimension_height = math.sqrt((-(b[0][2]+(-1*self.z_range[1]))*z_fac-(-b[4][2]+self.z_range[1])*z_fac)**2)
        
        temp = temp.transpose() + tr[:3, :1]
        temp = np.dot(sc[:3, :3], np.dot(rot[:3, :3], temp)).transpose()
        
        b = temp
        x0 = b[0][0]
        y0 = b[0][1]
        x1 = b[1][0]
        y1 = b[1][1]
        x2 = b[2][0]
        y2 = b[2][1]
        u0 = -(x0) * x_fac + self.size[0]
        v0 = -(y0 + self.size[2]) * y_fac + self.size[1]
        u1 = -(x1) * x_fac + self.size[0]
        v1 = -(y1 + self.size[2]) * y_fac + self.size[1]
        u2 = -(x2) * x_fac + self.size[0]
        v2 = -(y2 + self.size[2]) * y_fac + self.size[1]
        dimension_length2 = math.sqrt((v1-v2)**2 + (u1-u2)**2)
        dimension_width2 = math.sqrt((v1-v0)**2 + (u1-u0)**2)
        dimension_height2 = math.sqrt((-(b[0][2]+(-1*self.z_range[1]))*z_fac-(-b[4][2]+self.z_range[1])*z_fac)**2)
        
                
        return temp, dimension_length2/dimension_length, dimension_width2/dimension_width, dimension_height2/dimension_height
    