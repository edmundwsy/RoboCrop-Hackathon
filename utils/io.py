import open3d as o3d
import numpy as np

def save_pcd_file(filename, pcd):
  o3d.io.write_point_cloud(filename, pcd)

def read_ply_file(filenumber):
  filepath = "./data/" + filenumber + "_PCL.ply"
  pcd = o3d.io.read_point_cloud(filepath)
  return pcd