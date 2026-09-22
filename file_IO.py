def load_from_html(filename: str) -> list[dict]:
    """
    reads a dataset in HTML format. converts numeric data to float.
    raises an AttributeError if the rows don't all have the same number of values.
    """

    with open(filename, 'r') as file:
        contents = file.read()

    all_rows = []

    head, body = contents.split('</thead>')

    #get the column names
    head_parts = head.split('<td>')

    columns = []

    for column_name in head_parts[1:]:
        column_name = column_name.replace('</td>', '')
        column_name = column_name.replace('</tr>', '')
        columns.append(column_name.strip())

    #remove tags that aren't needed
    body = body.replace('</tr>', '')
    body = body.replace('</tbody>', '')
    body = body.replace('</table>', '')

    rows = body.split('<tr>')

    #go through each row
    for row in rows[1:]:
        row = row.replace('</td>', '')
        values = row.split('<td>')
        values = values[1:]

        #make sure the row has the right number of values
        if len(values) != len(columns):
            raise AttributeError(f'wrong number of values in row: {row}')

        row_dict = dict()

        for i in range(len(columns)):
            value = values[i].strip()

            #try to change numbers into floats
            try:
                value = float(value)
            except ValueError:
                pass

            row_dict[columns[i]] = value

        all_rows.append(row_dict)

    return all_rows

def split_csv_line(line: str) -> list[str]:
    values = []
    current_value = ''
    inside_quotes = False

    for character in line.strip():

        if character == '"':
            inside_quotes = not inside_quotes

        elif character == ',' and inside_quotes == False:
            values.append(current_value)
            current_value = ''

        else:
            current_value = current_value + character

    values.append(current_value)

    return values


def load_from_csv(filename: str) -> list[dict]:
    """
    reads a dataset in CSV format. converts numeric data to float.
    """

    all_rows = []

    with open(filename, 'r') as file:

        #first line has the column names
        first_line = file.readline()
        columns = split_csv_line(first_line)

        #go through the rest of the rows
        for line in file:
            values = split_csv_line(line)

            if len(values) != len(columns):
                raise Exception(
                    f'wrong number of values in row: {line.strip()}'
                )

            row_dict = dict()

            for i in range(len(columns)):
                value = values[i].strip()

                #try to change numbers into floats
                try:
                    value = float(value)
                except ValueError:
                    pass

                row_dict[columns[i].strip()] = value

            all_rows.append(row_dict)

    return all_rows

def save_to_json(data: list[dict], filename: str) -> None:
        """
        saves a dataset stored as a file as JSON format
        """

        with open(filename, 'w') as file:
            file.write('[')

            for i in range(len(data)):
                row = data[i]
                file.write('{')

                keys = list(row.keys())

                for j in range(len(keys)):
                    key = keys[j]
                    value = row[key]

                    file.write('"' + key + '": ')

                    if type(value) == str:
                        file.write('"' + value + '"')
                    else:
                        file.write(str(value))

                    if j < len(keys) - 1:
                        file.write(', ')

                file.write('}')

                if i < len(data) - 1:
                    file.write(', ')

            file.write(']')

def load_data(filename: str) -> list[dict]:
    """
    determines if a file is a CSV or HTML file and loads it accordingly
    """

    with open(filename, 'r') as file:
        first_part = file.read(1000)

    first_line = first_part.split('\n')[0]

    #check if the file is HTML
    if '<table' in first_part and '<thead>' in first_part:
        try:
            return load_from_html(filename)
        except Exception:
            raise Exception(
                'Error, data must be in valid CSV or HTML format'
            )

    #check if the file is CSV
    
    if ',' in first_line:
        try:
            return load_from_csv(filename)
        except Exception:
            raise Exception(
                'Error, data must be in valid CSV or HTML format'
            )


    raise Exception(
        'Error, data must be in valid CSV or HTML format'
    )