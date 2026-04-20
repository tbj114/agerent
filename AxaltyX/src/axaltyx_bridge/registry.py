ANALYSIS_REGISTRY = {
    # 描述统计
    "descriptive_stats": {
        "module": "axaltyx_core.descriptive",
        "function": "descriptive_stats",
        "category": "descriptive",
        "label_key": "analysis.descriptive_stats",
        "dialog": "DescriptiveDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "stats": {"type": "list[str]", "required": False, "default": ["mean", "std", "min", "max"], "source": "checkbox_group"}
        }
    },
    "frequencies": {
        "module": "axaltyx_core.frequency",
        "function": "frequencies",
        "category": "frequency",
        "label_key": "analysis.frequencies",
        "dialog": "FrequenciesDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "format": {"type": "str", "default": "table", "source": "radio_group"},
            "order": {"type": "str", "default": "ascending", "source": "radio_group"}
        }
    },
    "crosstabs": {
        "module": "axaltyx_core.crosstab",
        "function": "crosstabs",
        "category": "crosstab",
        "label_key": "analysis.crosstabs",
        "dialog": "CrosstabsDialog",
        "params_schema": {
            "row_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "col_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "layer_var": {"type": "str", "required": False, "source": "variable_selector_single"},
            "statistics": {"type": "list[str]", "required": False, "source": "checkbox_group"}
        }
    },
    "one_sample_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "one_sample_t",
        "category": "t_test",
        "label_key": "analysis.one_sample_t_test",
        "dialog": "OneSampleTDialog",
        "params_schema": {
            "var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "test_value": {"type": "float", "default": 0, "source": "number_input"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "independent_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "independent_t",
        "category": "t_test",
        "label_key": "analysis.independent_t_test",
        "dialog": "IndependentTDialog",
        "params_schema": {
            "test_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "group_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "equal_var": {"type": "bool", "default": True, "source": "checkbox"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "paired_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "paired_t",
        "category": "t_test",
        "label_key": "analysis.paired_t_test",
        "dialog": "PairedTDialog",
        "params_schema": {
            "var1": {"type": "str", "required": True, "source": "variable_selector_single"},
            "var2": {"type": "str", "required": True, "source": "variable_selector_single"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "one_way_anova": {
        "module": "axaltyx_core.anova",
        "function": "one_way_anova",
        "category": "anova",
        "label_key": "analysis.one_way_anova",
        "dialog": "OneWayAnovaDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "factor_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "post_hoc": {"type": "str", "default": None, "source": "dropdown"},
            "effect_size": {"type": "bool", "default": True, "source": "checkbox"}
        }
    },
    "linear_regression": {
        "module": "axaltyx_core.regression",
        "function": "linear_regression",
        "category": "regression",
        "label_key": "analysis.linear_regression",
        "dialog": "LinearRegressionDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "independent_vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "method": {"type": "str", "default": "enter", "source": "dropdown"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "logistic_regression": {
        "module": "axaltyx_core.regression",
        "function": "logistic_regression",
        "category": "regression",
        "label_key": "analysis.logistic_regression",
        "dialog": "LogisticRegressionDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "independent_vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "method": {"type": "str", "default": "enter", "source": "dropdown"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "exploratory_factor_analysis": {
        "module": "axaltyx_core.factor_analysis",
        "function": "exploratory_factor_analysis",
        "category": "dimension_reduction",
        "label_key": "analysis.efa",
        "dialog": "EFADialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "n_factors": {"type": "int", "default": "kaiser", "source": "number_or_auto"},
            "rotation": {"type": "str", "default": "varimax", "source": "dropdown"},
            "extraction": {"type": "str", "default": "principal_axis", "source": "dropdown"}
        }
    },
    "kmeans_clustering": {
        "module": "axaltyx_core.clustering",
        "function": "kmeans_clustering",
        "category": "classification",
        "label_key": "analysis.kmeans",
        "dialog": "KMeansDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "n_clusters": {"type": "int", "required": True, "source": "number_input"},
            "init": {"type": "str", "default": "k-means++", "source": "dropdown"},
            "standardize": {"type": "bool", "default": True, "source": "checkbox"}
        }
    },
    "kaplan_meier": {
        "module": "axaltyx_core.survival",
        "function": "kaplan_meier",
        "category": "survival",
        "label_key": "analysis.kaplan_meier",
        "dialog": "KaplanMeierDialog",
        "params_schema": {
            "time_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "event_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "group_var": {"type": "str", "required": False, "source": "variable_selector_single"},
            "conf_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "cronbach_alpha": {
        "module": "axaltyx_core.reliability",
        "function": "cronbach_alpha",
        "category": "reliability",
        "label_key": "analysis.cronbach_alpha",
        "dialog": "CronbachAlphaDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"}
        }
    }
}
