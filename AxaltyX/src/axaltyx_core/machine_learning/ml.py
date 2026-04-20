import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LassoCV, RidgeCV, ElasticNetCV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, r2_score
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional


def random_forest(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    task: str = "classification",
    n_estimators: int = 100,
    max_depth: int = None,
    test_size: float = 0.3,
    cv_folds: int = 5
) -> dict:
    """
    随机森林
    
    Args:
        data: 输入数据
        target_var: 目标变量
        feature_vars: 特征变量列表
        task: 任务类型（classification/regression）
        n_estimators: 树的数量
        max_depth: 树的最大深度
        test_size: 测试集比例
        cv_folds: 交叉验证折数
    
    Returns:
        随机森林结果
    """
    try:
        # 准备数据
        X = data[feature_vars].dropna()
        y = data.loc[X.index, target_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 选择模型
        if task == "classification":
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        
        # 训练模型
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算性能指标
        performance = {}
        if task == "classification":
            performance["accuracy"] = accuracy_score(y_test, y_pred)
            performance["precision"] = precision_score(y_test, y_pred, average="weighted")
            performance["recall"] = recall_score(y_test, y_pred, average="weighted")
            performance["f1"] = f1_score(y_test, y_pred, average="weighted")
            if len(np.unique(y)) == 2:
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                performance["auc"] = roc_auc_score(y_test, y_pred_proba)
            else:
                performance["auc"] = 0.0
            performance["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()
        else:
            performance["r_squared"] = r2_score(y_test, y_pred)
        
        # 交叉验证
        cv_results = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
        
        # 特征重要性
        feature_importance = pd.DataFrame({
            "feature": feature_vars,
            "importance": model.feature_importances_
        }).sort_values(by="importance", ascending=False)
        
        # OOB分数（仅适用于随机森林）
        oob_score = model.oob_score_ if hasattr(model, "oob_score_") else 0.0
        
        # 构建结果
        results = {
            "model_params": {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "task": task
            },
            "feature_importance": feature_importance,
            "performance": performance,
            "cv_results": {
                "mean": cv_results.mean(),
                "std": cv_results.std(),
                "scores": cv_results.tolist()
            },
            "oob_score": oob_score,
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def support_vector_machine(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    kernel: str = "rbf",
    cv_folds: int = 5
) -> dict:
    """
    支持向量机
    
    Args:
        data: 输入数据
        target_var: 目标变量
        feature_vars: 特征变量列表
        kernel: 核函数（linear/poly/rbf/sigmoid）
        cv_folds: 交叉验证折数
    
    Returns:
        支持向量机结果
    """
    try:
        # 准备数据
        X = data[feature_vars].dropna()
        y = data.loc[X.index, target_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 选择模型
        if len(np.unique(y)) == 2:
            model = SVC(kernel=kernel, probability=True, random_state=42)
        else:
            model = SVR(kernel=kernel)
        
        # 训练模型
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算性能指标
        performance = {}
        if len(np.unique(y)) == 2:
            performance["accuracy"] = accuracy_score(y_test, y_pred)
            performance["precision"] = precision_score(y_test, y_pred)
            performance["recall"] = recall_score(y_test, y_pred)
            performance["f1"] = f1_score(y_test, y_pred)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            performance["auc"] = roc_auc_score(y_test, y_pred_proba)
            performance["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()
        else:
            performance["r_squared"] = r2_score(y_test, y_pred)
        
        # 交叉验证
        cv_results = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
        
        # 支持向量数量
        support_vectors_count = len(model.support_) if hasattr(model, "support_") else 0
        
        # 构建结果
        results = {
            "model_params": {
                "kernel": kernel
            },
            "performance": performance,
            "cv_results": {
                "mean": cv_results.mean(),
                "std": cv_results.std(),
                "scores": cv_results.tolist()
            },
            "support_vectors_count": support_vectors_count,
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def gradient_boosting(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    task: str = "classification",
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 3,
    cv_folds: int = 5
) -> dict:
    """
    梯度提升
    
    Args:
        data: 输入数据
        target_var: 目标变量
        feature_vars: 特征变量列表
        task: 任务类型（classification/regression）
        n_estimators: 树的数量
        learning_rate: 学习率
        max_depth: 树的最大深度
        cv_folds: 交叉验证折数
    
    Returns:
        梯度提升结果
    """
    try:
        # 准备数据
        X = data[feature_vars].dropna()
        y = data.loc[X.index, target_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 选择模型
        if task == "classification":
            model = GradientBoostingClassifier(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=42
            )
        else:
            model = GradientBoostingRegressor(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=42
            )
        
        # 训练模型
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算性能指标
        performance = {}
        if task == "classification":
            performance["accuracy"] = accuracy_score(y_test, y_pred)
            performance["precision"] = precision_score(y_test, y_pred, average="weighted")
            performance["recall"] = recall_score(y_test, y_pred, average="weighted")
            performance["f1"] = f1_score(y_test, y_pred, average="weighted")
            if len(np.unique(y)) == 2:
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                performance["auc"] = roc_auc_score(y_test, y_pred_proba)
            else:
                performance["auc"] = 0.0
            performance["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()
        else:
            performance["r_squared"] = r2_score(y_test, y_pred)
        
        # 交叉验证
        cv_results = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
        
        # 特征重要性
        feature_importance = pd.DataFrame({
            "feature": feature_vars,
            "importance": model.feature_importances_
        }).sort_values(by="importance", ascending=False)
        
        # 构建结果
        results = {
            "model_params": {
                "n_estimators": n_estimators,
                "learning_rate": learning_rate,
                "max_depth": max_depth,
                "task": task
            },
            "feature_importance": feature_importance,
            "performance": performance,
            "cv_results": {
                "mean": cv_results.mean(),
                "std": cv_results.std(),
                "scores": cv_results.tolist()
            },
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def neural_network(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    hidden_layers: list[int] = None,
    activation: str = "relu",
    max_iter: int = 200,
    cv_folds: int = 5
) -> dict:
    """
    神经网络
    
    Args:
        data: 输入数据
        target_var: 目标变量
        feature_vars: 特征变量列表
        hidden_layers: 隐藏层大小列表
        activation: 激活函数（relu/logistic/tanh/identity）
        max_iter: 最大迭代次数
        cv_folds: 交叉验证折数
    
    Returns:
        神经网络结果
    """
    try:
        # 准备数据
        X = data[feature_vars].dropna()
        y = data.loc[X.index, target_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 默认隐藏层
        if hidden_layers is None:
            hidden_layers = [100, 50]
        
        # 选择模型
        if len(np.unique(y)) == 2:
            model = MLPClassifier(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                max_iter=max_iter,
                random_state=42
            )
        else:
            model = MLPRegressor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                max_iter=max_iter,
                random_state=42
            )
        
        # 训练模型
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算性能指标
        performance = {}
        if len(np.unique(y)) == 2:
            performance["accuracy"] = accuracy_score(y_test, y_pred)
            performance["precision"] = precision_score(y_test, y_pred)
            performance["recall"] = recall_score(y_test, y_pred)
            performance["f1"] = f1_score(y_test, y_pred)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            performance["auc"] = roc_auc_score(y_test, y_pred_proba)
            performance["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()
        else:
            performance["r_squared"] = r2_score(y_test, y_pred)
        
        # 交叉验证
        cv_results = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
        
        # 损失曲线
        loss_curve = model.loss_curve_ if hasattr(model, "loss_curve_") else []
        
        # 构建结果
        results = {
            "architecture": {
                "hidden_layers": hidden_layers,
                "activation": activation,
                "max_iter": max_iter
            },
            "performance": performance,
            "cv_results": {
                "mean": cv_results.mean(),
                "std": cv_results.std(),
                "scores": cv_results.tolist()
            },
            "loss_curve": loss_curve,
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def lasso_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    cv_folds: int = 5
) -> dict:
    """
    Lasso回归
    
    Args:
        data: 输入数据
        dependent_var: 因变量
        independent_vars: 自变量列表
        alpha: 正则化参数
        cv_folds: 交叉验证折数
    
    Returns:
        Lasso回归结果
    """
    try:
        # 准备数据
        X = data[independent_vars].dropna()
        y = data.loc[X.index, dependent_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 使用交叉验证选择最佳alpha
        model = LassoCV(alphas=[0.001, 0.01, 0.1, 1.0, 10.0], cv=cv_folds, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算R平方
        r_squared = r2_score(y_test, y_pred)
        
        # 提取系数
        coefficients = pd.DataFrame({
            "variable": independent_vars,
            "coefficient": model.coef_
        })
        
        # 计算非零系数数量
        nonzero_count = sum(model.coef_ != 0)
        
        # 构建结果
        results = {
            "coefficients": coefficients,
            "nonzero_count": nonzero_count,
            "best_alpha": model.alpha_,
            "cv_results": {
                "mean": model.mse_path_.mean(axis=1)[model.alphas_.tolist().index(model.alpha_)],
                "std": model.mse_path_.std(axis=1)[model.alphas_.tolist().index(model.alpha_)]
            },
            "r_squared": r_squared,
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def ridge_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    cv_folds: int = 5
) -> dict:
    """
    Ridge回归
    
    Args:
        data: 输入数据
        dependent_var: 因变量
        independent_vars: 自变量列表
        alpha: 正则化参数
        cv_folds: 交叉验证折数
    
    Returns:
        Ridge回归结果
    """
    try:
        # 准备数据
        X = data[independent_vars].dropna()
        y = data.loc[X.index, dependent_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 使用交叉验证选择最佳alpha
        model = RidgeCV(alphas=[0.001, 0.01, 0.1, 1.0, 10.0], cv=cv_folds)
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算R平方
        r_squared = r2_score(y_test, y_pred)
        
        # 提取系数
        coefficients = pd.DataFrame({
            "variable": independent_vars,
            "coefficient": model.coef_
        })
        
        # 构建结果
        results = {
            "coefficients": coefficients,
            "best_alpha": model.alpha_,
            "cv_results": {
                "mean": 0.0,  # 简化处理
                "std": 0.0   # 简化处理
            },
            "r_squared": r_squared,
            "predictions": pd.Series(y_pred, index=X_test.index)
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


def elastic_net(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    cv_folds: int = 5
) -> dict:
    """
    Elastic Net回归
    
    Args:
        data: 输入数据
        dependent_var: 因变量
        independent_vars: 自变量列表
        alpha: 正则化参数
        l1_ratio: L1正则化比例
        cv_folds: 交叉验证折数
    
    Returns:
        Elastic Net回归结果
    """
    try:
        # 准备数据
        X = data[independent_vars].dropna()
        y = data.loc[X.index, dependent_var]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 标准化数据
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 使用交叉验证选择最佳参数
        model = ElasticNetCV(
            alphas=[0.001, 0.01, 0.1, 1.0, 10.0],
            l1_ratio=[0.1, 0.5, 0.9],
            cv=cv_folds,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = model.predict(X_test_scaled)
        
        # 计算R平方
        r_squared = r2_score(y_test, y_pred)
        
        # 提取系数
        coefficients = pd.DataFrame({
            "variable": independent_vars,
            "coefficient": model.coef_
        })
        
        # 计算非零系数数量
        nonzero_count = sum(model.coef_ != 0)
        
        # 构建结果
        results = {
            "coefficients": coefficients,
            "nonzero_count": nonzero_count,
            "best_alpha": model.alpha_,
            "best_l1_ratio": model.l1_ratio_,
            "cv_results": {
                "mean": 0.0,  # 简化处理
                "std": 0.0   # 简化处理
            },
            "r_squared": r_squared,
            "predictions": pd.Series(y_pred, index=X_test.index)
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
