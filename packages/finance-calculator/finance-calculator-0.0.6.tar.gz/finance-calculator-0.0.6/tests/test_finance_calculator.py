from src.finance_calculator import api as fc
from src.finance_calculator.cli import main
from tests.test_nav_data import scheme_data, benchmark_data


def test_ratio_calculator():
    rc = fc.get_ratio_calculator(scheme_data, benchmark_data)
    dwd = rc.get_alpha(365*3)


def test_benchmark_nav_created_from_risk_free_rate():
    rc = fc.get_ratio_calculator(scheme_data, risk_free_rate=0.05)


def test_drawdown():
    drawdown = fc.get_drawdown(scheme_data)
    assert drawdown is not None
    assert type(drawdown) is float


def test_volatility():
    vol = fc.get_volatility(scheme_data)
    assert vol is not None
    assert type(vol) is float


def test_sharpe():
    sharpe = fc.get_sharpe(scheme_data, benchmark_data)
    assert sharpe is not None
    assert type(sharpe) is float


def test_sortino():
    sortino = fc.get_sortino(scheme_data, benchmark_data)
    assert sortino is not None
    assert type(sortino) is float


def test_upside_capture():
    up_capture = fc.get_upside_capture(scheme_data, benchmark_data)
    assert up_capture is not None
    assert type(up_capture) is float


def test_downside_capture():
    down_capture = fc.get_downside_capture(scheme_data, benchmark_data)
    assert down_capture is not None
    assert type(down_capture) is float


def test_beta():
    beta = fc.get_beta(scheme_data, benchmark_data)
    assert beta is not None
    assert type(beta) is float


def test_treynor():
    treynor = fc.get_treynor(scheme_data, benchmark_data)
    assert treynor is not None
    assert type(treynor) is float


def test_alpha():
    alpha = fc.get_alpha(scheme_data, benchmark_data)
    assert alpha is not None
    assert type(alpha) is float


def test_main():
    assert main([]) == 0
