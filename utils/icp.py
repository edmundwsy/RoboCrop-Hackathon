import numpy as np
import open3d as o3d
import copy

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])


def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
      source_down, 
      target_down, 
      source_fpfh, 
      target_fpfh, 
      True,
      distance_threshold,
      o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
      3, 
      [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
      o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)], 
      o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999)
    )
    return result


def global_registration_test(pc1, pc2):
  print("Load a ply point cloud, print it, and render it")
  print("Project point cloud 2 to point cloud 1")
  trans_init = np.diag([1,1,1,1])
  draw_registration_result(pc1, pc2, trans_init)
  pc2.transform(trans_init)

  voxel_size = 0.05
  pc1_down, pc1_fpfh = preprocess_point_cloud(pc1, voxel_size)
  pc2_down, pc2_fpfh = preprocess_point_cloud(pc2, voxel_size)

  result_ransac = global_registration(pc2_down, pc1_down, pc2_fpfh, pc1_fpfh, voxel_size)
  draw_registration_result(pc2, pc1, result_ransac.transformation) 


def draw_registration_result_original_color(source, target, transformation):
    source_temp = copy.deepcopy(source)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target])

def fast_global_registration(pc1, pc2):
  voxel_size = 0.01  # means 1cm for the dataset
  pc1_down, pc1_fpfh = preprocess_point_cloud(pc1, voxel_size)
  pc2_down, pc2_fpfh = preprocess_point_cloud(pc2, voxel_size)
  distance_threshold = voxel_size * 0.5
  print(":: Apply fast global registration with distance threshold %.3f" \
            % distance_threshold)
  result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(
        pc2_down, 
        pc1_down, 
        pc2_fpfh, 
        pc1_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold)
        )
  print(result)
  return result

def two_cloud_icp(pc1, pc2):
    identity_transform = np.identity(4)
    print(identity_transform)
    # draw_registration_result_original_color(pc2, pc1, identity_trasform)
    fast_result = fast_global_registration(pc1, pc2)
    init_transform = fast_result.transformation
    print("Transformation is:")
    print(init_transform)    
    # draw_registration_result_original_color(pc2, pc1, init_transform)

    print("Apply point-to-point ICP")
    threshold = 0.02
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pc2, pc1, threshold, init_transform,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)

    icp_transform = reg_p2p.transformation
    print("Transformation is:")
    print(icp_transform)
    # draw_registration_result_original_color(pc2, pc1, icp_transform)
    return icp_transform