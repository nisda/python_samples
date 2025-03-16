
import mylibs.dict_util as dict_util
import pytest
import re


@pytest.fixture
def product_data():
    product_data:dict = {
        "id" : 1,
        "product" : {
            "name" : "AX0016",
            "category" : ["101", "102"],
            "price" : 123456,
        },
        "created" : {
            "user" : {
                "id" : "A0001",
                "name" : "alan",
            },
            "date" : "2025-01-22",
        },
        "updated" : {
            "user" : {
                "id" : "B0001",
                "name" : "Bobby",
            },
            "date" : "2025-03-02",
        },
    }
    return product_data


def test_dict_mapping(product_data:dict):
    mapping_dict:dict = {
        "id" : "id",
        "product_name" : "product.name",
        "price" : ("product", "price"),
        "category" : "product.category",
        "start_date" : "product.start_date.is_not_exists",
        "end_date" : None,
        "created_user" : {
            "id" : "created.user.id",
            "name" : ("created", "user", "name"),
        },
        "created_date" : "created.date",
        "updated_user" : {
            "id" : "updated.user.id",
            "name" : ("updated", "user", "name"),
        },
        "updated_date" : "updated.date",
    }
    ret = dict_util.dict_mapping(data_dict=product_data, mapping_dict=mapping_dict)
    assert ret == {
        "id" : 1,
        "product_name" : "AX0016",
        "price" : 123456,
        "category" : ["101", "102"],
        "start_date" : None,
        "end_date" : None,
        "created_user" : {
            "id" : "A0001",
            "name" : "alan",
        },
        "created_date" : "2025-01-22",
        "updated_user" : {
            "id" : "B0001",
            "name" :  "Bobby",
        },
        "updated_date" : "2025-03-02",
    }


def test_dict_mapping_key_path_separator(product_data:dict):
    mapping_dict:dict = {
        "id" : "id",
        "product_name" : "product/name",
        "price" : ("product", "price"),
        "category" : "product.category",
    }
    ret = dict_util.dict_mapping(data_dict=product_data, mapping_dict=mapping_dict, key_path_separator="/")
    assert ret == {
        "id" : 1,
        "product_name" : "AX0016",
        "price" : 123456,
        "category" : None,
    }
