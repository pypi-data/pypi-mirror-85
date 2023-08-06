import pytest
import hejmdal
# import testhelper

def test_get_file_base():
    result = hejmdal.main.get_data(BFE='on')
    assert isinstance(result, hejmdal.datacalls.Data)
    assert isinstance(result, hejmdal.datacalls.FileData)
    assert isinstance(result, hejmdal.datacalls.DownloadableData)
    assert isinstance(result, hejmdal.datacalls.SmartSourceData)
    assert isinstance(result, hejmdal.datacalls.JsonData)
    assert isinstance(result.data, str) or isinstance(result.data, bytes)
    assert isinstance(result.data_out, dict)

