import numpy as np
import pandas as pd

from arch.unitroot import ADF
from statsmodels.tsa.api import VAR
from statsmodels.tsa.base.datetools import dates_from_str

import seaborn as sns
import matplotlib.pyplot as plt

sns.set()