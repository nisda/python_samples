import dynamodb_util
import sys
from pprint import pprint

TABLE_NAME = "test-20260128"
# TABLE_NAME = "apigw-poc-apigw-basic-auth"



if __name__ == '__main__':
    table:dynamodb_util.Table = dynamodb_util.Table(table_name=TABLE_NAME, ttl_default=60)
    pprint(table.pk_schema)
    pprint(table.gsi_schemas)
    pprint(table.lsi_schemas)
    pprint(table.ttl_name)
    pprint(table.ttl_default)

    pprint("-----------")
    pprint(list(table.scan()))

    pprint("-----------")
    pprint(list(table.query2(key={'pk': 'p1', 'sk': 's3'})))

    pprint("-----------")
    pprint(list(table.query2(key={'pk': 'p1'}, index_name="LSI-01")))

    pprint("-----------")
    pprint(list(table.query2(key={'pk': 'p1', 'lsi_sk': 'ls1', 'gsi_sk': 'gss2'}, index_name="LSI-01")))

    pprint("-----------")
    pprint(list(table.query2(key={'gsi_pk': 'gip2'}, index_name="GSI-01")))

    pprint("-----------")
    pprint(table.get_item(key={'pk': 'p1', 'sk': 's5'}))

    pprint("-----------")
    pprint(table.put_item(item={'pk': 'p3', 'sk': 's1', 'biko': 'B'}, ttl=30))

    pprint("-----------")
    pprint(table.put_item(item={'pk': 'p3', 'sk': 's1', 'biko': 'BB'}, ttl=30, overwrite=False))

    pprint("-----------")
    pprint(table.put_item(item={'pk': 'p3', 'sk': 's1', 'biko': 'BBB'}, ttl=0))

    pprint("-----------")
    pprint(table.put_items(items=[
        {'pk': 'p4', 'sk': 's1', 'biko': 'C'},
        {'pk': 'p4', 'sk': 's2', 'biko': 'CC'},
        {'pk': 'p4', 'sk': 's3', 'biko': 'CCC'},
    ], ttl=20))

    pprint("-----------")
    pprint(table.delete_item(key={'pk': 'p3', 'sk': 's1', 'biko': 'BBB'}))

    pprint("-----------")
    pprint(table.delete_item(key={'pk': 'p3', 'sk': 's1', 'biko': 'BBB'}))
    sys.exit(0)
