import numpy as np
import open3d

def remove_outliers(cloud, nb_neighbours=10, std_ratio=1.0):
  cl, ind = cloud.remove_statistical_outlier(nb_neighbors=10, std_ratio=1.0)
  new = cloud.select_by_index(ind)
  return new