import random
import numpy as np
from scipy.spatial.transform import Rotation as R

def get_augmentation_parameters(augment, 
                                image_translate_x_p=1., 
                                image_translate_y_p=1.,
                                translate_x_p=1., 
                                translate_y_p=1., 
                                translate_z_p=1.,
                                ang_p=1.,
                                scale_x_p=1.,
                                scale_y_p=1.,
                                fliplr_p=0.5,
                                bev_add_noise_p=0.3,
                                bev_dropout_noise_p=0.3,
                                bev_cutout_p=0.3
                                ):
    if augment:

        if np.random.random_sample() >= (1. - image_translate_x_p):
            image_translate_x = random.randint(-50, 50)
        else:
            image_translate_x = 0
        if np.random.random_sample() >= (1. - image_translate_y_p):
            image_translate_y = random.randint(-25, 25)
        else:
            image_translate_y = 0

        if np.random.random_sample() >= (1. - translate_x_p):
            translate_x = random.randint(-5, 5)
        else:
            translate_x = 0
        if np.random.random_sample() >= (1. - translate_y_p):
            translate_y = random.randint(-5, 5)
        else:
            translate_y = 0

        if np.random.random_sample() >= (1. - translate_z_p):
            translate_z = random.random() - 0.5
        else:
            translate_z = 0

        if np.random.random_sample() >= (1. - ang_p):
            ang = random.randint(-45, 45)
        else:
            ang = 0

        r = R.from_rotvec(np.radians(ang) * np.array([0, 0, 1]))
        rot = r.as_dcm()
        rot = np.append(rot, np.array([[0,0,0]]), axis=0)
        rot = np.append(rot, np.array([[0],[0],[0],[1]]), axis=1)

        tr_x = translate_x
        tr_y = translate_y
        tr_z = translate_z
        tr = np.array([[tr_x], [tr_y], [tr_z], [0]])
        
        translate_x = 0
        translate_y = 0
        translate_z = 0
        
        sc_x = 1
        sc_y = 1
        sc_z = 1

        if np.random.random_sample() >= (1. - scale_x_p):
           sc_x += ((random.random() * 2) - 1.) / 10.

        if np.random.random_sample() >= (1. - scale_y_p):
           sc_y += ((random.random() * 2) - 1.) / 10.


        sc = np.array([[sc_x, 0, 0, 0], [0, sc_y, 0, 0], [0, 0, sc_z, 0], [0, 0, 0, 1]])

        fliplr = np.random.random_sample() >= (1. - fliplr_p)

        bev_add_noise = np.random.random_sample() >= (1. - bev_add_noise_p)
        bev_dropout_noise = np.random.random_sample() >= (1. - bev_dropout_noise_p)
        bev_cutout = np.random.random_sample() >= (1. - bev_cutout_p)

    else:
        image_translate_x = 0
        image_translate_y = 0

        translate_x = 0
        translate_y = 0
        translate_z = 0
        ang = 0

        r = R.from_rotvec(np.radians(0) * np.array([0, 0, 1]))
        rot = r.as_dcm()
        rot = np.append(rot, np.array([[0,0,0]]), axis=0)
        rot = np.append(rot, np.array([[0],[0],[0],[1]]), axis=1)

        tr_x = 0
        tr_y = 0
        tr_z = 0
        tr = np.array([[tr_x], [tr_y], [tr_z], [0]])

        sc_x = 1
        sc_y = 1
        sc_z = 1
        sc = np.array([[sc_x, 0, 0, 0], [0, sc_y, 0, 0], [0, 0, sc_z, 0], [0, 0, 0, 1]])

        fliplr = False
        bev_add_noise = False
        bev_dropout_noise = False
        bev_cutout = False

    return rot, tr, sc, image_translate_x, image_translate_y, ang, fliplr, bev_add_noise, bev_dropout_noise, bev_cutout
