
# coding: utf-8

class SimpleTable:


    def __init__(self, header=[], rows=[]):
        self._header = header
        self._rows = rows


    def set_header(self, header):
        self._header = header


    def set_rows(self, rows):
        self._rows = rows


    def add_row(self, row):
        self._rows.append(row)


    def print_table(self, indent=0):
        print(self.get_table(indent))


    def get_table(self, indent=0):
        table = None
        if ( len(self._rows) > 0 ):
            obj = self._rows[0]
            if isinstance(obj, list) or isinstance(obj, tuple):
                table = self._generate_table_from_list(indent)
            if isinstance(obj, dict):
                table = self._generate_table_from_dict(indent)
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


    def _generate_table_from_list(self, indent=0):
        header = self._header or []
        rows   = self._rows or []

        column_count = max(max([len(v) for v in rows]), len(header))
        length_table = [ [] for x in range(0, column_count) ]

        for i in range(0, len(header)):
            length_table[i].append(self._get_unicode_width(header[i]))

        for row in rows:
            for i in range(0, len(row)):
                length_table[i].append(self._get_unicode_width(row[i]))

        column_lengths = [ max(x) for x in length_table ]

        lines = []
        border = "+" + "+".join([ ("-" * ( x + 2 )) for x in column_lengths ]) + "+"

        if ( len(header) > 0 ):
            lines.append(border)
            header = [ self._padding(header[i] if i < len(header) else "", column_lengths[i]) for i in range(0, len(column_lengths)) ]
            lines.append( "| " + " | ".join(header) + " |" )

        lines.append(border)
        for row in rows:
            row = [ self._padding(row[i] if i < len(row) else "", column_lengths[i]) for i in range(0, len(column_lengths)) ]
            lines.append( "| " + " | ".join(row) + " |" )
        lines.append(border)

        table = (" " * indent) + ("\n" + (" " * indent)).join(lines)

        return table


    def _generate_table_from_dict(self, indent=0):

        header = self._header or []
        rows   = self._rows or []

        if ( len(header) > 0):
            keys = []
            captions = {}
            for h in header:
                if ( isinstance(h, list) or isinstance(h, tuple) ):
                    key = h[0] if len(h) > 0 else ""
                    caption = h[1] if len(h) > 1 else key
                    keys.append(key)
                    captions[key] = caption
                else:
                    keys.append(h)
                    captions[h] = h
        else:
            keys = [ k for r in rows for k in r.keys() ]
            keys = sorted(set(keys), key=keys.index)
            captions = { v:v for v in keys }

        column_lengths = {}
        for key in keys:
            column_lengths[key] = max( self._get_unicode_width(row.get(key, None)) for row in rows )
            column_lengths[key] = max( column_lengths[key], self._get_unicode_width(captions[key]) )

        lines = []
        border = "+" + "+".join([ ("-" * ( x + 2 )) for x in column_lengths.values() ]) + "+"

        lines.append(border)
        header = [ self._padding(captions[key], column_lengths[key]) for key in keys ]
        lines.append( "| " + " | ".join(header) + " |" )

        lines.append(border)
        for row in rows:
            row = [ self._padding(row.get(key, None), column_lengths[key]) for key in keys ]
            lines.append( "| " + " | ".join(row) + " |" )
        lines.append(border)

        table = (" " * indent) + ("\n" + (" " * indent)).join(lines)

        return table
