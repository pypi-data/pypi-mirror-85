from .bev_reader import *
from .calib_reader import *
from .image_reader import *
from .label_reader import *
from .aug_utils import *

class DataReader:

    def __init__(self, 
                    image_path, 
                    calib_path, 
                    label_path, 
                    lidar_path, 
                    param_object):

        rot, tr, sc, translate_x, translate_y, ang, fliplr, bev_add_noise, bev_dropout_noise, bev_cutout = get_augmentation_parameters(param_object.augment, 
                                image_translate_x_p=param_object.image_translate_x_p, 
                                image_translate_y_p=param_object.image_translate_y_p,
                                translate_x_p=param_object.translate_x_p, 
                                translate_y_p=param_object.translate_y_p, 
                                translate_z_p=param_object.translate_z_p,
                                ang_p=param_object.ang_p,
                                scale_x_p=param_object.scale_x_p,
                                scale_y_p=param_object.scale_y_p,
                                fliplr_p=param_object.fliplr_p,
                                bev_add_noise_p=param_object.bev_add_noise_p,
                                bev_dropout_noise_p=param_object.bev_dropout_noise_p,
                                bev_cutout_p=param_object.bev_cutout_p
                                )
        self.image_path = image_path
        self.calib_path = calib_path
        self.label_path = label_path
        self.lidar_path = lidar_path

        self.bev_reader = BEVReader(lidar_path, calib_path, image_path, rot, tr, sc, 
                        fliplr=fliplr, 
                        bev_add_noise=bev_add_noise, 
                        bev_dropout_noise=bev_dropout_noise, 
                        bev_cutout=bev_cutout,
                        interpolate=param_object.interpolate,
                        x_range=param_object.x_range, 
                        y_range=param_object.y_range, 
                        z_range=param_object.z_range, 
                        size=param_object.bev_size)
        self.image_reader = ImageReader(image_path, translate_x, translate_y, image_size=param_object.image_size)
        self.calib_reader = CalibReader(calib_path)
        self.label_reader = LabelReader(label_path, calib_path, rot, tr, sc, ang, self.calib_reader,
                                        x_range=param_object.x_range, 
                                        y_range=param_object.y_range, 
                                        z_range=param_object.z_range, 
                                        size=param_object.bev_size, 
                                        get_actual_dims=param_object.get_actual_dims, 
                                        from_file=param_object.from_file, fliplr=fliplr)

 
    def read_lidar(self):
        return self.lidar_reader.read_lidar()

    def read_calib(self):
        return self.calib_reader.read_calib()

    def read_image(self):
        return self.image_reader.read_image()

    def read_label(self):
        return self.label_reader.read_label()
    