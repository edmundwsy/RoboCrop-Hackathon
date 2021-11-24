import numpy as np
import open3d as o3d
from utils.io import *

# print("Testing IO for point cloud ...")
# pcd = o3d.io.read_point_cloud("./data/1_PCL.ply")
# print(pcd)
# o3d.io.write_point_cloud("copy_of_fragment.pcd", pcd)



if __name__ == "__main__":

  print("Load a ply point cloud, print it, and render it")
  pc1 = read_ply_file("1")
  o3d.visualization.draw_geometries([pc1],
                                    zoom=0.3412,
                                    front=[0.4257, -0.2125, -0.8795],
                                    lookat=[2.6172, 2.0475, 1.532],
                                    up=[-0.0694, -0.9768, 0.2024])

  print("Downsample the point cloud with a voxel of 0.02")
  voxel_down_pcd = pc1.voxel_down_sample(voxel_size=0.02)
  o3d.visualization.draw_geometries([voxel_down_pcd],
                                    zoom=0.3412,
                                    front=[0.4257, -0.2125, -0.8795],
                                    lookat=[2.6172, 2.0475, 1.532],
                                    up=[-0.0694, -0.9768, 0.2024])