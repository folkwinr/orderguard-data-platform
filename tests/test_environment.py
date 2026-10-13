import sys
import pandas as pd

def test_python_environment():
    assert sys.version_info.major == 3

def test_pandas():
    numbers = pd.Series([10, 20, 30])
    assert numbers.sum() == 60