import pytest
from unittest.mock import patch

from swc_visualizer import visualize_swc
from swc_visualizer.processing import swc_to_dataframe, dataframe_to_tree


# ---------- Fixtures ----------


@pytest.fixture
def valid_swc_file(tmp_path):
    filepath = tmp_path / "valid.swc"
    filepath.write_text(
        """# sample neuron
1 1 0.0 0.0 0.0 1.0 -1
2 1 1.0 0.0 0.0 0.5 1
3 1 2.0 0.0 0.0 0.4 2
4 1 1.0 1.0 0.0 0.6 2
"""
    )
    return filepath


@pytest.fixture
def invalid_swc_missing_parent(tmp_path):
    filepath = tmp_path / "missing_parent.swc"
    filepath.write_text(
        """1 1 0 0 0 1 -1
2 1 1 0 0 1 3
"""
    )
    return filepath


# ---------- Tests ----------


def test_swc_parsing(valid_swc_file):
    df = swc_to_dataframe(valid_swc_file)
    root, nodes = dataframe_to_tree(df)

    # Basic tree structure
    assert root._index == 1
    assert len(nodes) == 4
    assert len(root._children) == 1
    assert root._children[0]._index == 2


def test_missing_parent_raises_error(invalid_swc_missing_parent):
    df = swc_to_dataframe(invalid_swc_missing_parent)

    with pytest.raises(ValueError, match="Parent index 3 not found"):
        dataframe_to_tree(df)


def test_tree_metrics(valid_swc_file):
    df = swc_to_dataframe(valid_swc_file)
    root, nodes = dataframe_to_tree(df)

    # Node 3 is two edges of length 1.0 from the root.
    assert nodes[3].distance_from_root() == pytest.approx(2.0)

    # Total tree length = 1.0 + 1.0 + 1.0
    assert root.total_length() == pytest.approx(3.0)


@patch("matplotlib.pyplot.show")
@patch("plotly.graph_objects.Figure.show")
def test_visualization_runs(
    mock_plotly_show,
    mock_plt_show,
    valid_swc_file,
):
    # Ensure both visualization functions run without raising exceptions.
    visualize_swc(str(valid_swc_file), visualization="2d")
    visualize_swc(str(valid_swc_file), visualization="3d")
