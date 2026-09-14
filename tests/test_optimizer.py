import pytest
import pandas as pd
import numpy as np
from solarnex_bess.data_generator import generate_market_data
from solarnex_bess.optimizer import SolarnexBESSOptimizer

def test_data_generation():
    df = generate_market_data(days=2)
    assert len(df) == 48
    assert 'price' in df.columns
    assert 'load' in df.columns

def test_optimizer_initial_state():
    optimizer = SolarnexBESSOptimizer(capacity_mwh=10.0, max_power_mw=2.5, rte=0.90)
    df_window = generate_market_data(days=1).head(24)
    result = optimizer.optimize_window(df_window)
    
    # Check if SoC respects boundaries
    assert (result['soc'] >= 0).all()
    assert (result['soc'] <= optimizer.capacity).all()
    
    # Check charge/discharge power limits
    assert (result['p_charge'] <= optimizer.max_power).all()
    assert (result['p_discharge'] <= optimizer.max_power).all()
