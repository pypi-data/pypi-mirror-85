"""
"""
from .context import read_csv


def test_read_csv():
    # valid include
    assert read_csv('tests/csv_tables.csv', '') is not None
    # check type
    data = r"""1,2
3,4
"""
    assert read_csv(None, data) == [
        ['1', '2'],
        ['3', '4']
    ]
    # check complex cells
    data = r"""asdfdfdfguhfdhghfdgkla,"334
2",**la**,4
5,6,7,8"""
    assert read_csv(None, data) == [
        ['asdfdfdfguhfdhghfdgkla', '334\n2', '**la**', '4'],
        ['5', '6', '7', '8']
    ]
    # check include
    assert read_csv('tests/csv_tables.csv',
                     data) == [['**_Fruit_**',
                                '~~Price~~',
                                '_Number_',
                                '`Advantages`'],
                               ['*Bananas~1~*',
                                '$1.34',
                                '12~units~',
                                'Benefits of eating bananas \n(**Note the appropriately\nrendered block markdown**):    \n\n- _built-in wrapper_        \n- ~~**bright color**~~\n\n'],
                               ['*Oranges~2~*',
                                '$2.10',
                                '5^10^~units~',
                                'Benefits of eating oranges:\n\n- **cures** scurvy\n- `tasty`']]

    # check encoding
    assert read_csv('tests/csv_table_gbk.csv',
                     data, encoding='gbk') == [
        ['一', '二', '三'],
        ['a', 'b', 'c'],
        ['1', '2', '3']]
    return
