import validators

from page_analyzer.database import DataBase


def is_valid_url(url: str) -> bool:
    '''
    Castom validator for url
    '''
    if len(url) <= 255:
        return validators.url(url)

    return False


def get_urls_(db_url, name_table, clause_where):
    '''
    Get table inromation about urls
    '''
    db = DataBase(db_url)
    return db.get_data_table(name_table, clause_where=clause_where)


def get_url_checks(db_url, name_table, clause_where):
    '''
    Get table inromation about cheks url
    '''
    db = DataBase(db_url)
    return db.get_data_table(name_table,
                             clause_where=clause_where,
                             clause_order='created_at')


def add_url_(db_url, name_table, name_fields, data_fields):
    '''
    Add inromation in table
    '''
    db = DataBase(db_url)
    db.change_table(name_table, name_fields, data_fields)


def get_pivot_urls_information(db_url):
    '''
    Get pivot table inromation about urls
    '''
    db = DataBase(db_url)
    return db.left_join_urls_and_url_cheks()
