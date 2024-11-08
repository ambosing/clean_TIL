from sqlalchemy import inspect


def row_to_dict(row) -> dict:
    print(inspect(row))
    print(inspect(row).attrs)
    print(inspect(row).attrs.keys())

    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}
