import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from typing import Dict, Any, List, Optional


def hierarchical_clustering(
    data: pd.DataFrame,
    vars: list[str],
    method: str = "ward",
    metric: str = "euclidean",
    n_clusters: int = None
) -> dict:
    """
    层次聚类分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        method: 链接方法（ward/complete/average/single/centroid/median）
        metric: 距离度量（euclidean/cityblock/cosine/correlation）
        n_clusters: 聚类数（None 则不切割）
    
    Returns:
        层次聚类分析结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        X_scaled = StandardScaler().fit_transform(X)
        
        # 计算链接矩阵
        linkage_matrix = linkage(X_scaled, method=method, metric=metric)
        
        # 计算距离矩阵
        distance_matrix = pdist(X_scaled, metric=metric)
        
        # 生成聚类结果
        clusters = None
        cluster_sizes = None
        silhouette = None
        
        if n_clusters is not None:
            model = AgglomerativeClustering(n_clusters=n_clusters, linkage=method, metric=metric)
            clusters = model.fit_predict(X_scaled)
            cluster_sizes = {i: sum(clusters == i) for i in range(n_clusters)}
            if n_clusters > 1:
                silhouette = silhouette_score(X_scaled, clusters)
        
        # 构建结果
        results = {
            "linkage_matrix": linkage_matrix.tolist(),
            "dendrogram_data": {},  # 简化处理
            "clusters": clusters,
            "cluster_sizes": cluster_sizes,
            "distance_matrix": distance_matrix.tolist(),
            "silhouette_score": silhouette
        }
        
        return {
            "success": True,
            "results": results,
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def kmeans_clustering(
    data: pd.DataFrame,
    vars: list[str],
    n_clusters: int,
    init: str = "k-means++",
    n_init: int = 10,
    max_iter: int = 300,
    standardize: bool = True
) -> dict:
    """
    K均值聚类分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        n_clusters: 聚类数
        init: 初始化方法（k-means++/random）
        n_init: 初始中心数量
        max_iter: 最大迭代次数
        standardize: 是否标准化数据
    
    Returns:
        K均值聚类分析结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        
        # 标准化数据
        if standardize:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
        else:
            X_scaled = X.values
        
        # 执行K均值聚类
        kmeans = KMeans(
            n_clusters=n_clusters,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            random_state=42
        )
        kmeans.fit(X_scaled)
        
        # 提取结果
        labels = kmeans.labels_
        cluster_centers = pd.DataFrame(
            kmeans.cluster_centers_,
            columns=vars,
            index=[f"Cluster {i+1}" for i in range(n_clusters)]
        )
        
        # 计算聚类评估指标
        silhouette = silhouette_score(X_scaled, labels)
        calinski_harabasz = calinski_harabasz_score(X_scaled, labels)
        davies_bouldin = davies_bouldin_score(X_scaled, labels)
        
        # 计算聚类大小
        cluster_sizes = {i: sum(labels == i) for i in range(n_clusters)}
        
        # 构建结果
        results = {
            "cluster_centers": cluster_centers,
            "cluster_sizes": cluster_sizes,
            "labels": pd.Series(labels, index=X.index),
            "inertia": kmeans.inertia_,
            "silhouette_score": silhouette,
            "calinski_harabasz_score": calinski_harabasz,
            "davies_bouldin_score": davies_bouldin,
            "n_clusters": n_clusters,
            "iterations": kmeans.n_iter_,
            "converged": kmeans.n_iter_ < max_iter
        }
        
        return {
            "success": True,
            "results": results,
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def two_step_clustering(
    data: pd.DataFrame,
    vars: list[str],
    distance_measure: str = "log_likelihood",
    auto_determine_clusters: bool = True,
    max_clusters: int = 15
) -> dict:
    """
    两步聚类分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        distance_measure: 距离度量（log_likelihood/euclidean）
        auto_determine_clusters: 是否自动确定聚类数
        max_clusters: 最大聚类数
    
    Returns:
        两步聚类分析结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        X_scaled = StandardScaler().fit_transform(X)
        
        # 简化处理，使用K均值作为替代
        # 自动确定聚类数（简化处理）
        optimal_n = 2
        if auto_determine_clusters:
            # 使用轮廓系数选择最优聚类数
            best_silhouette = -1
            for k in range(2, min(max_clusters, len(X))):
                kmeans = KMeans(n_clusters=k, random_state=42)
                labels = kmeans.fit_predict(X_scaled)
                silhouette = silhouette_score(X_scaled, labels)
                if silhouette > best_silhouette:
                    best_silhouette = silhouette
                    optimal_n = k
        else:
            optimal_n = max_clusters
        
        # 执行聚类
        kmeans = KMeans(n_clusters=optimal_n, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        
        # 计算聚类中心
        cluster_centers = pd.DataFrame(
            kmeans.cluster_centers_,
            columns=vars,
            index=[f"Cluster {i+1}" for i in range(optimal_n)]
        )
        
        # 计算聚类大小
        cluster_sizes = {i: sum(labels == i) for i in range(optimal_n)}
        
        # 计算轮廓系数
        silhouette = silhouette_score(X_scaled, labels)
        
        # 构建BIC/IC表（简化处理）
        bic_ic_table = {}
        
        # 构建结果
        results = {
            "clusters": labels,
            "cluster_sizes": cluster_sizes,
            "cluster_centers": cluster_centers,
            "silhouette": silhouette,
            "bic_ic_table": bic_ic_table,
            "optimal_n": optimal_n
        }
        
        return {
            "success": True,
            "results": results,
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def dbscan_clustering(
    data: pd.DataFrame,
    vars: list[str],
    eps: float = 0.5,
    min_samples: int = 5
) -> dict:
    """
    DBSCAN聚类分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        eps: 邻域半径
        min_samples: 最小样本数
    
    Returns:
        DBSCAN聚类分析结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        X_scaled = StandardScaler().fit_transform(X)
        
        # 执行DBSCAN聚类
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X_scaled)
        
        # 计算聚类数和噪声点
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = sum(labels == -1)
        
        # 计算聚类大小
        cluster_sizes = {}
        for label in set(labels):
            if label != -1:
                cluster_sizes[label] = sum(labels == label)
        
        # 提取核心样本
        core_samples = dbscan.core_sample_indices_
        
        # 构建结果
        results = {
            "labels": labels,
            "n_clusters": n_clusters,
            "n_noise": n_noise,
            "cluster_sizes": cluster_sizes,
            "core_samples": core_samples.tolist()
        }
        
        return {
            "success": True,
            "results": results,
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }
