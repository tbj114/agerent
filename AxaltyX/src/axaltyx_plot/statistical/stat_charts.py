import pandas as pd
import numpy asimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graphimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipyimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import rocimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plotimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "normimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().values
        x = np.sort(x)
        
        # 计算经验分布
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().values
        x = np.sort(x)
        
        # 计算经验分布
        n = len(x)
        empirical = np.arange(1, n+1) /import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().values
        x = np.sort(x)
        
        # 计算经验分布
        n = len(x)
        empirical = np.arange(1, n+1) / n
        
        # 计算理论分布
        if dist == "norm":
            # 正态分布
            mu,import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().values
        x = np.sort(x)
        
        # 计算经验分布
        n = len(x)
        empirical = np.arange(1, n+1) / n
        
        # 计算理论分布
        if dist == "norm":
            # 正态分布
            mu, sigma = stats.norm.fit(x)
            theoretical = stats.norm.cdf(x, muimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    try:
        apply_theme("arco")
        fig, ax = plt.subplots(figsize=figsize)
        
        # 准备数据
        x = data[var].dropna().values
        x = np.sort(x)
        
        # 计算经验分布
        n = len(x)
        empirical = np.arange(1, n+1) / n
        
        # 计算理论分布
        if dist == "norm":
            # 正态分布
            mu, sigma = stats.norm.fit(x)
            theoretical = stats.norm.cdf(x, mu, sigma)
        elif dist == "ex