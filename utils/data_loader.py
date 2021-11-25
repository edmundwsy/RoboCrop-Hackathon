import open3d as o3d
import numpy as np

def save_pcd_file(filename, pcd):
  o3d.io.write_point_cloud(filename, pcd)

def read_ply_file(filenumber):
  filepath = "./data/" + filenumber + "_PCL.ply"
  pcd = o3d.io.read_point_cloud(filepath)
  return pcd

def convert_nparray(pcd):
  # np_points = np.asarray(pcd.points)
  np_colors = np.asarray(pcd.colors)
  # return np.hstack([np_points, np_colors])
  return np_colors

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