import pandas as pd
import numpy as np
import networkx as nx

def network_analysis(data: pd.DataFrame, source_var: str, target_var: str, weight_var: str = None) -> dict:
    try:
        # 检查变量是否存在
        for var in [source_var, target_var]:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        if weight_var and weight_var not in data.columns:
            raise ValueError(f"变量 {weight_var} 不存在于数据中")
        
        # 创建图
        if weight_var:
            # 带权重的图
            edges = list(zip(data[source_var], data[target_var], data[weight_var]))
            G = nx.Graph()
            G.add_weighted_edges_from(edges)
        else:
            # 无权重的图
            edges = list(zip(data[source_var], data[target_var]))
            G = nx.Graph()
            G.add_edges_from(edges)
        
        # 计算基本统计量
        nodes = G.number_of_nodes()
        edges = G.number_of_edges()
        
        # 计算密度
        if nodes > 1:
            density = nx.density(G)
        else:
            density = 0
        
        # 计算中心性指标
        centrality = {
            "degree": dict(nx.degree_centrality(G)),
            "betweenness": dict(nx.betweenness_centrality(G)),
            "closeness": dict(nx.closeness_centrality(G)),
            "eigenvector": dict(nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06))
        }
        
        # 社区检测（使用Girvan-Newman算法）
        communities = []
        try:
            from networkx.algorithms.community import girvan_newman
            comp = girvan_newman(G)
            # 获取第一个划分
            first_partition = next(comp)
            communities = [list(c) for c in first_partition]
        except ImportError:
            # 如果没有networkx社区模块，使用简单的连通组件
            communities = list(nx.connected_components(G))
        
        communities_dict = {f"community_{i}": list(community) for i, community in enumerate(communities)}
        
        # 计算组件数
        components = nx.number_connected_components(G)
        
        # 计算聚类系数
        clustering_coefficient = nx.average_clustering(G)
        
        # 计算平均路径长度
        try:
            avg_path_length = nx.average_shortest_path_length(G)
        except nx.NetworkXError:
            # 对于不连通的图，计算每个组件的平均路径长度并加权平均
            avg_path_lengths = []
            sizes = []
            for component in nx.connected_components(G):
                subgraph = G.subgraph(component)
                if len(component) > 1:
                    avg_path_lengths.append(nx.average_shortest_path_length(subgraph))
                    sizes.append(len(component))
            if sizes:
                avg_path_length = np.average(avg_path_lengths, weights=sizes)
            else:
                avg_path_length = 0
        
        return {
            "success": True,
            "results": {
                "nodes": nodes,
                "edges": edges,
                "density": float(density),
                "centrality": centrality,
                "communities": communities_dict,
                "components": components,
                "clustering_coefficient": float(clustering_coefficient),
                "avg_path_length": float(avg_path_length)
            },
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
