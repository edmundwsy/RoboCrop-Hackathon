import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import normalize, scale, MinMaxScaler
from data_loader import convert_nparray, read_ply_file

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

def histogram_analysis(pc):
    pcd = copy.deepcopy(pc)
    voxel_size = 0.01
    pcd = pcd.voxel_down_sample(voxel_size)
    np_pcd = convert_nparray(pcd)

    plt.figure()
    plt.subplot(1, 3, 1)
    plot_histogram(np_pcd[:, 0])
    plt.subplot(1, 3, 2)
    plot_histogram(np_pcd[:, 1])
    plt.subplot(1, 3, 3)
    plot_histogram(np_pcd[:, 2])
    plt.savefig("histogram.png")
    # plt.show()


def segmentation(pc):
    pcd = copy.deepcopy(pc)
    voxel_size = 0.01
    pcd = pcd.voxel_down_sample(voxel_size)
    np_pcd = convert_nparray(pcd)
    # normed_pcd = np_pcd - np.min(np_pcd, axis=0) / (np.max(np_pcd, axis=0) - np.min(np_pcd, axis=0))
    # normed_pcd = scale(np_pcd,  axis=1, with_mean=True,
    #                    with_std=False, copy=True)
    normed_pcd = MinMaxScaler().fit_transform(np_pcd)
    # cls = DBSCAN(eps=1e-3, min_samples=10, metric='euclidean', metric_params=None,
    #                     algorithm='kd_tree', leaf_size=30, p=None, n_jobs=16)
    cls = KMeans(n_clusters=4)
    clustering = cls.fit(normed_pcd)
    labels = clustering.labels_

    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")
    colors = plt.get_cmap("tab20")(
        labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    # o3d.visualization.draw_geometries([pcd])

    return pcd

def plot_histogram(x):
    q25, q75 = np.percentile(x, [25, 75])
    bin_width = 2 * (q75 - q25) * len(x) ** (-1/3)
    bins = round((x.max() - x.min()) / bin_width)
    bins = 100
    plt.hist(x, density=True, bins=bins)  # density=False would make counts



if __name__ == "__main__":
    pc1 = read_ply_file("1")
    pc1 = remove_outliers(pc1)
    pc2 = segmentation(pc1)

    o3d.visualization.draw_geometries([pc2])