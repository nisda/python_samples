
import mylibs.dict_util as dict_util
import pytest
import re


@pytest.fixture
def mapping_dict():
    mapping_dict:dict = {
        "A" : 1,
        "B" : None,
        "C" : {
            "CA" : 5,
            "CB" : {
                "CBA" : 2,
                "CBB" : None,
                "CBC" : 3,
            },
        },
        "D" : 4,
    }
    return mapping_dict


def test_auto_order_same(mapping_dict:dict):
    input_data:list = ["101", "102", "103", "104", "105", "106", "107"]
    ret = dict_util.list_mapping(data_list=input_data, mapping_dict=mapping_dict, auto_order=True)
    assert ret == {
        "A" : "101",
        "B" : "102",
        "C" : {
            "CA" : "103",
            "CB" : {
                "CBA" : "104",
                "CBB" : "105",
                "CBC" : "106",
            },
        },
        "D" : "107",
    }


def test_auto_order_few(mapping_dict:dict):
    input_data:list = ["101", "102", "103", "104", "105"]
    ret = dict_util.list_mapping(data_list=input_data, mapping_dict=mapping_dict, auto_order=True)
    assert ret == {
        "A" : "101",
        "B" : "102",
        "C" : {
            "CA" : "103",
            "CB" : {
                "CBA" : "104",
                "CBB" : "105",
                "CBC" : None,
            },
        },
        "D" : None,
    }



def test_specify_order(mapping_dict:dict):
    input_data:list = ["100", "101", "102", "103", "104"]
    ret = dict_util.list_mapping(data_list=input_data, mapping_dict=mapping_dict, auto_order=False)
    assert ret == {
        "A" : "101",
        "B" : None,
        "C" : {
            "CA" : None,
            "CB" : {
                "CBA" : "102",
                "CBB" : None,
                "CBC" : "103",
            },
        },
        "D" : "104",
    }
