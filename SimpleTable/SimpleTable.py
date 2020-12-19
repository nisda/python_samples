
# coding: utf-8

class SimpleTable:


    def __init__(self, header=[], rows=[]):
        self._header = header
        self._rows = rows
        self._CAPTION_OF_NO_DATA = "(no data)"


    def set_header(self, header):
        self._header = header


    def set_rows(self, rows):
        self._rows = rows


    def add_row(self, row):
        self._rows.append(row)


    def print_table(self, indent=0):
        print(self.get_table(indent))


    def get_table(self, indent=0):
        table = self._generate_table(indent)
        return table


    def _get_unicode_width(self, value):
        import unicodedata
        width = {'F': 2, 'W': 2, 'A': 2}
        s = self._to_str(value)
        return sum(width.get(unicodedata.east_asian_width(c), 1) for c in s)


    def _to_str(self, value):
        value = "" if value is None else str(value)
        return value


    def _padding(self, value, length, alignment="auto", spacer=" "):

        alignment = alignment.lower()
        if ( alignment == "auto" ):
            if ( isinstance(value, int) or isinstance(value, float) ):
                alignment = "right"
            else:
                alignment = "left"

        value = self._to_str(value)

        spacer = (spacer[0] * (length - self._get_unicode_width(value)))
        if ( alignment == "left" ):
            result = value + spacer
        if ( alignment == "right" ):
            result = spacer + value

        return result


    def _generate_table(self, indent=0):
        # None のときは空リストに置き換え
        header = self._header or []
        rows   = self._rows or []

        if ( len(rows) == 0 ):
            return self._CAPTION_OF_NO_DATA


        # dict or list ?
        is_dict = ( len(rows) > 0 and isinstance(rows[0], dict) )

        # dict 且つヘッダ未指定の場合は、全データのkeyからヘッダを生成。
        if ( is_dict and len(header) == 0 ):
            keys = [ k for r in rows for k in r.keys() ]
            header = sorted(set(keys), key=keys.index)

        # ヘッダの属性情報を補完
        temp = []
        for col in header:
            if ( isinstance(col, list) or isinstance(col, tuple) ):
                key         = col[0]    if len(col) > 0 else ""
                caption     = col[1]    if len(col) > 1 else key
                alignment   = col[2]    if len(col) > 2 else "auto"
            else:
                key         = col
                caption     = col
                alignment   = "auto"
            temp.append({
                "key" : key,
                "caption" : caption,
                "alignment" : alignment.lower(),
            })
        header = temp

        # list(list) 型に統一。データをヘッダに合わせて整列。
        if ( is_dict ):
            records = [ [r.get(h["key"], None) for h in header ] for r in rows ]
        elif ( len(header) == 0 ):
            column_count = max([ len(r) for r in rows ])
            records = [ [ r[i] if i < len(r) else None for i in range(0, column_count) ] for r in rows ]
        else:
            column_count = len(header)
            records = [ [ r[i] if i < len(r) else None for i in range(0, column_count) ] for r in rows ]

        # 各列の最大長を算出
        if ( len(records) > 0 ):
            column_count = max(len(records[0]), len(header))
        else:
            column_count = len(header)

        length_table = [ [] for x in range(0, column_count) ]

        for i in range(0, len(header)):
            length_table[i].append(self._get_unicode_width(header[i].get("caption", None)))

        for row in records:
            for i in range(0, len(row)):
                length_table[i].append(self._get_unicode_width(row[i]))

        column_lengths = [ max(x) for x in length_table ]


        # テーブル文字列を生成

        lines = []
        border = "+" + "+".join([ ("-" * ( x + 2 )) for x in column_lengths ]) + "+"

        if ( len(header) > 0 ):
            lines.append(border)
            header = [ self._padding(header[i].get("caption", None) if i < len(header) else "", column_lengths[i]) for i in range(0, len(column_lengths)) ]
            lines.append( "| " + " | ".join(header) + " |" )

        lines.append(border)
        if ( len(records) > 0 ):
            for row in records:
                row = [ self._padding(row[i] if i < len(row) else "", column_lengths[i]) for i in range(0, len(column_lengths)) ]
                lines.append( "| " + " | ".join(row) + " |" )
            lines.append(border)

        table = (" " * indent) + ("\n" + (" " * indent)).join(lines)

        return table


        return None


