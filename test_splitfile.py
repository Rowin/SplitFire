import PyPDF2
from splitfire import get_split_intervals, export_page_range
from unittest import mock


def test_get_split_interval_various_index():
    assert get_split_intervals([], 10) == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    assert get_split_intervals([2], 10) == [[1], [2, 3, 4, 5, 6, 7, 8, 9, 10]]
    assert get_split_intervals([2, 4], 10) == [[1], [2, 3], [4, 5, 6, 7, 8, 9, 10]]
    assert get_split_intervals([2, 10], 10) == [[1], [2, 3, 4, 5, 6, 7, 8, 9], [10]]


def test_export_page_range(mocker):
    inputpdf = mocker.MagicMock()
    inputpdf.getPage = mocker.MagicMock()
    mocker.patch("PyPDF2.pdf.PdfFileWriter")
    mocker.patch.object(PyPDF2.PdfFileWriter, "addPage")
    m = mocker.mock_open()
    export_page_range(inputpdf, [1, 2], "out.pdf")

    inputpdf.getPage.assert_any_call(1)
    inputpdf.getPage.assert_any_call(2)
