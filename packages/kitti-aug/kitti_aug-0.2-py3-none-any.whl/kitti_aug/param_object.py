class ParamObject(object):

    def __init__(self):
        self.get_default_params()

    def get_default_params(self):
        self.get_actual_dims=False
        self.from_file=True
        self.bev_size=(448, 512, 35)
        self.interpolate=False
        self.x_range=(0, 70)
        self.y_range=(-40, 40) 
        self.z_range=(-2.5, 1)
        self.image_size=(370, 1224)
        self.augment=False
        self.image_translate_x_p=1.
        self.image_translate_y_p=1.
        self.translate_x_p=1.
        self.translate_y_p=1. 
        self.translate_z_p=1.
        self.ang_p=1.
        self.scale_x_p=1.
        self.scale_y_p=1.
        self.fliplr_p=0.5
        self.bev_add_noise_p=0.3
        self.bev_dropout_noise_p=0.3
        self.bev_cutout_p=0.3
        self.bev_cutout_x_size=5
        self.bev_cutout_y_size=5
        self.bev_cutout_z_size=2
        self.bev_cutout_n_squares=1