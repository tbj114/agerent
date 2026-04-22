from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QIcon
from src.axaltyx_i18n.manager import I18nManager


class NavigationPanel(QWidget):
    """左侧导航面板"""

    sig_analysis_selected = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.init_ui()
        self.init_navigation_tree()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setIndentation(20)
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                border: none;
                background-color: #F7F8FA;
            }
            QTreeWidget::item {
                height: 36px;
                padding-left: 12px;
            }
            QTreeWidget::item:selected {
                background-color: #E8F3FF;
                color: #165DFF;
                border-left: 3px solid #165DFF;
            }
            QTreeWidget::item:hover {
                background-color: #F2F3F5;
            }
        """)
        self.tree_widget.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.tree_widget)
        self.setLayout(layout)
        self.setMinimumWidth(200)
        self.setMaximumWidth(300)

    def init_navigation_tree(self):
        # 分析分类数据
        categories = [
            {
                'id': 'descriptive',
                'label': self.i18n.get_text('navigation.categories.descriptive'),
                'items': [
                    {'id': 'descriptive_stats', 'label': self.i18n.get_text('navigation.items.descriptive_stats')},
                    {'id': 'frequencies', 'label': self.i18n.get_text('navigation.items.frequencies')}
                ]
            },
            {
                'id': 'crosstabs',
                'label': self.i18n.get_text('navigation.categories.crosstabs'),
                'items': [
                    {'id': 'crosstabs', 'label': self.i18n.get_text('navigation.items.crosstabs')}
                ]
            },
            {
                'id': 'means_comparison',
                'label': self.i18n.get_text('navigation.categories.means'),
                'items': []
            },
            {
                'id': 't_test',
                'label': self.i18n.get_text('navigation.categories.t_test'),
                'items': [
                    {'id': 'one_sample_t', 'label': self.i18n.get_text('navigation.items.one_sample_t')},
                    {'id': 'independent_t', 'label': self.i18n.get_text('navigation.items.independent_t')},
                    {'id': 'paired_t', 'label': self.i18n.get_text('navigation.items.paired_t')}
                ]
            },
            {
                'id': 'anova',
                'label': self.i18n.get_text('navigation.categories.anova'),
                'items': [
                    {'id': 'one_way_anova', 'label': self.i18n.get_text('navigation.items.one_way_anova')},
                    {'id': 'two_way_anova', 'label': self.i18n.get_text('navigation.items.two_way_anova')},
                    {'id': 'ancova', 'label': self.i18n.get_text('navigation.items.ancova')},
                    {'id': 'rm_anova', 'label': self.i18n.get_text('navigation.items.rm_anova')}
                ]
            },
            {
                'id': 'nonparametric',
                'label': self.i18n.get_text('navigation.categories.nonparametric'),
                'items': [
                    {'id': 'mann_whitney', 'label': self.i18n.get_text('navigation.items.mann_whitney')},
                    {'id': 'wilcoxon', 'label': self.i18n.get_text('navigation.items.wilcoxon')},
                    {'id': 'kruskal_wallis', 'label': self.i18n.get_text('navigation.items.kruskal_wallis')},
                    {'id': 'friedman', 'label': self.i18n.get_text('navigation.items.friedman')}
                ]
            },
            {
                'id': 'correlation',
                'label': self.i18n.get_text('navigation.categories.correlation'),
                'items': [
                    {'id': 'pearson', 'label': self.i18n.get_text('navigation.items.pearson')},
                    {'id': 'partial_corr', 'label': self.i18n.get_text('navigation.items.partial_corr')},
                    {'id': 'spearman', 'label': self.i18n.get_text('navigation.items.spearman')}
                ]
            },
            {
                'id': 'regression',
                'label': self.i18n.get_text('navigation.categories.regression'),
                'items': [
                    {'id': 'linear_reg', 'label': self.i18n.get_text('navigation.items.linear_reg')},
                    {'id': 'logistic_reg', 'label': self.i18n.get_text('navigation.items.logistic_reg')},
                    {'id': 'ordinal_reg', 'label': self.i18n.get_text('navigation.items.ordinal_reg')},
                    {'id': 'nonlinear_reg', 'label': self.i18n.get_text('navigation.items.nonlinear_reg')},
                    {'id': 'curve_est', 'label': self.i18n.get_text('navigation.items.curve_est')}
                ]
            },
            {
                'id': 'dimension_reduction',
                'label': self.i18n.get_text('navigation.categories.dimension_reduction'),
                'items': [
                    {'id': 'efa', 'label': self.i18n.get_text('navigation.items.efa')},
                    {'id': 'cfa', 'label': self.i18n.get_text('navigation.items.cfa')},
                    {'id': 'pca', 'label': self.i18n.get_text('navigation.items.pca')}
                ]
            },
            {
                'id': 'classification',
                'label': self.i18n.get_text('navigation.categories.classification'),
                'items': [
                    {'id': 'hierarchical_cluster', 'label': self.i18n.get_text('navigation.items.hierarchical_cluster')},
                    {'id': 'kmeans', 'label': self.i18n.get_text('navigation.items.kmeans')},
                    {'id': 'discriminant', 'label': self.i18n.get_text('navigation.items.discriminant')}
                ]
            },
            {
                'id': 'survival',
                'label': self.i18n.get_text('navigation.categories.survival'),
                'items': [
                    {'id': 'kaplan_meier', 'label': self.i18n.get_text('navigation.items.kaplan_meier')},
                    {'id': 'cox_reg', 'label': self.i18n.get_text('navigation.items.cox_reg')}
                ]
            },
            {
                'id': 'advanced',
                'label': self.i18n.get_text('navigation.categories.advanced'),
                'items': [
                    {'id': 'random_forest', 'label': self.i18n.get_text('navigation.items.random_forest')},
                    {'id': 'svm', 'label': self.i18n.get_text('navigation.items.svm')},
                    {'id': 'meta_analysis', 'label': self.i18n.get_text('navigation.items.meta_analysis')}
                ]
            }
        ]

        # 构建树
        for category in categories:
            category_item = QTreeWidgetItem(self.tree_widget)
            category_item.setText(0, category['label'])
            category_item.setData(0, Qt.ItemDataRole.UserRole, {
                'type': 'category',
                'id': category['id']
            })
            
            for item in category['items']:
                sub_item = QTreeWidgetItem(category_item)
                sub_item.setText(0, item['label'])
                sub_item.setData(0, Qt.ItemDataRole.UserRole, {
                    'type': 'item',
                    'id': item['id']
                })

        # 展开第一个分类
        if self.tree_widget.topLevelItemCount() > 0:
            self.tree_widget.expandItem(self.tree_widget.topLevelItem(0))

    def on_item_clicked(self, item, column):
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if item_data and item_data['type'] == 'item':
            self.sig_analysis_selected.emit(item_data['id'], {})

    def set_collapsed(self, collapsed):
        if collapsed:
            self.setMinimumWidth(48)
            self.setMaximumWidth(48)
        else:
            self.setMinimumWidth(200)
            self.setMaximumWidth(300)

    def toggle_collapse(self):
        current_max = self.maximumWidth()
        if current_max <= 50:
            self.set_collapsed(False)
        else:
            self.set_collapsed(True)
