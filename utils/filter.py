import numpy as np
import open3d as o3d

def remove_outliers(cloud, nb_neighbours=10, std_ratio=1.0):
  # min_bound = np.array([-0.4, -0.25, -0.9])
  # max_bound = np.array([0.4, 0.3, -0.35])
  bbox = o3d.geometry.AxisAlignedBoundingBox(
    min_bound=(-0.4, -0.25, -0.9), 
    max_bound=(0.4, 0.3, -0.35)
    )
  cloud = cloud.crop(bbox)
  cl, ind = cloud.remove_statistical_outlier(nb_neighbors=10, std_ratio=1.0)
  new = cloud.select_by_index(ind)
  return new