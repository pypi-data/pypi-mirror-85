
# KITTIAug

## Usage
```

import kitti_aug

param_object = kitti_aug.ParamObject()
param_object.augment = True

image_path = ""
calib_path = ""
label_path = ""
lidar_path = ""
data_reader_obj = kitti_aug.DataReader(image_path, 
                    calib_path, 
                    label_path, 
                    lidar_path, 
                    param_object)

camera_image = data_reader_obj.read_image()
lidar_image = data_reader_obj.lidar_reader.read_lidar()
real_points, label = data_reader_obj.label_reader.read_label()

```
