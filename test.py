import numpy as np
import open3d as o3d
from utils.data_loader import *
from utils.icp import *
from utils.filter import *

# print("Testing IO for point cloud ...")
# pcd = o3d.io.read_point_cloud("./data/1_PCL.ply")
# print(pcd)
# o3d.io.write_point_cloud("copy_of_fragment.pcd", pcd)


pc1 = read_ply_file("1")
pc1 = remove_outliers(pc1)
# pc2 = read_ply_file("5")
# pc2 = remove_outliers(pc2)
# trans = two_cloud_icp(pc1, pc2)
# pc2.transform(trans)
# o3d.visualization.draw_geometries([pc1])
pc2 = segmentation(pc1)

# trans = np.array(
#     [[1, 0, 0, -0.282],
#     [0, 1, 0, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1]]
#     )
# trans = two_cloud_p2p(pc1, pc2)

o3d.visualization.draw_geometries([pc2])