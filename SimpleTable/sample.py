# coding: utf-8
import sys
import SimpleTable


if __name__ == "__main__":

    print("")
    print("### list or tuple - No column specified")
    table = SimpleTable.SimpleTable()
    table.set_rows(
        [
            ("a", "b", "c"),
            ["あいう", "かきくけ", "さしすせそ", "たちつ", "なにぬ", "はひふへ"],
            [1, 2, "3", "4"],
            [123, 2345, 345.77, 456.0]
        ]
    )
    table.print_table()


    print("")
    print("### list or tuple - Column specified (too many)")

    table = SimpleTable.SimpleTable()
    table.set_header(["A","B","C","D","E","F","G", "H"])
    table.set_rows(
        [
            ("a", "b", "c"),
            ["あいう", "かきくけ", "さしすせそ", "たちつ", "なにぬ", "はひふへ"],
            [1, 2, "3", "4"],
            [123, 2345, 345.77, 456.0]
        ]
    )
    table.print_table()


    print("")
    print("### list or tuple - Column specified (too few)")

    table = SimpleTable.SimpleTable()
    table.set_header(["A","B","C","D"])
    table.set_rows(
        [
            ("a", "b", "c"),
            ["あいう", "かきくけ", "さしすせそ", "たちつ", "なにぬ", "はひふへ"],
            [1, 2, "3", "4"],
            [123, 2345, 345.77, 456.0]
        ]
    )
    table.print_table()


    print("")
    print("### dict - No column specified")

    table = SimpleTable.SimpleTable()
    table.set_rows(
        [
            {"id": 1, "name": "abc"},
            {"id": 2, "name": "あいうえお", "value": 412},
            {"id": 3, "name": "かきくkekooooo", "value": 9},
            {"id": 100, "description": "abcd", "invisible": "Visible if no column is specified", "value": "123"},
        ]
    )
    table.print_table()

    print("")
    print("### dict - Column specified")

    table = SimpleTable.SimpleTable()
    table.set_header(["id", ("name", "表示名"), ("description"), ["value", "ポイント"]])
    table.set_rows(
        [
            {"id": 1, "name": "abc"},
            {"id": 2, "name": "あいうえお", "value": 412},
            {"id": 3, "name": "かきくkekooooo", "value": 9},
            {"id": 100, "description": "abcd", "invisible": "Visible if no column is specified", "value": "123"},
        ]
    )
    table.print_table()


    print("")
    print("### with indent")

    table = SimpleTable.SimpleTable()
    table.set_header(["id", ("name", "表示名"), ("description"), ["value", "ポイント"]])
    table.set_rows(
        [
            {"id": 1, "name": "abc"},
            {"id": 2, "name": "あいうえお", "value": 412},
            {"id": 3, "name": "かきくkekooooo", "value": 9},
            {"id": 100, "description": "abcd", "invisible": "Visible if no column is specified", "value": "123"},
        ]
    )
    table.print_table(4)


    print("")
    print("### brank(row)")

    table = SimpleTable.SimpleTable()
    table.set_header(["id", "name"])
    table.print_table()


    print("")
    print("### brank(both)")

    table = SimpleTable.SimpleTable()
    table.set_rows([])
    table.print_table()


    sys.exit(0)
