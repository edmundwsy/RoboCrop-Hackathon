import numpy as np
import open3d as o3d
from utils.io import *
from utils.icp import *
from utils.filter import *

# print("Testing IO for point cloud ...")
# pcd = o3d.io.read_point_cloud("./data/1_PCL.ply")
# print(pcd)
# o3d.io.write_point_cloud("copy_of_fragment.pcd", pcd)


# pc1 = read_ply_file("4")
# pc2 = read_ply_file("5")
# pc1 = remove_outliers(pc1)
# pc2 = remove_outliers(pc2)
# trans = two_cloud_icp(pc1, pc2)
# pc2.transform(trans)
# o3d.visualization.draw_geometries([pc1, pc2])




print("Load a ply point cloud, print it, and render it")
pc1 = read_ply_file("1")
# pc2 = read_ply_file("2")
pc1 = remove_outliers(pc1)
# pc2 = remove_outliers(pc2)
cloud_list = [pc1]

trans = np.array(
    [[1, 0, 0, -0.14],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]]
    )
pc0 = pc1
# for i in range(2, 14):
for i in range(2, 14):
    print("=" * 20)
    print("Project point cloud ", i, " to point cloud 1")
    pci = read_ply_file(str(i))
    pci = remove_outliers(pci)
    trans = two_cloud_p2p(pc0, pci)
    # for _ in range(i-1):
    pci.transform(trans)
    cloud_list.append(pci)
    pc0 = pci

o3d.visualization.draw_geometries(cloud_list)



