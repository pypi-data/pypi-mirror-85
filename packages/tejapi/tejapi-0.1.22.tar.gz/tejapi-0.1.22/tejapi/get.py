from tejapi.model.datatable import Datatable
from tejapi.errors.tej_error import LimitExceededError
from tejapi.api_config import ApiConfig
from tejapi.message import Message
import warnings
import copy

def get(datatable_code, **options):
    
    if 'paginate' in options.keys():
        paginate = options.pop('paginate')
    else:
        paginate = None
        
    if 'chinese_column_name' in options.keys():
        chinese_column_name = options.pop('chinese_column_name')
    else:
        chinese_column_name = False
        
    if 'opts_filter' in options.keys():
        filters = options.pop('opts_filter')
        options.update(filters)

    data = None
    page_count = 0
    while True:
        next_options = copy.deepcopy(options)
        next_data = Datatable(datatable_code).data(params=next_options)

        if data is None:
            data = next_data
        else:
            data.extend(next_data)

        if page_count >= ApiConfig.page_limit:
            raise LimitExceededError(Message.WARN_DATA_LIMIT_EXCEEDED)

        next_cursor_id = next_data.meta['next_cursor_id']

        if next_cursor_id is None:
            break
        elif paginate is not True and next_cursor_id is not None:
            warnings.warn(Message.WARN_PAGE_LIMIT_EXCEEDED, UserWarning)
            break

        page_count = page_count + 1
        options['opts.cursor_id'] = next_cursor_id
        
    return data.to_pandas(chinese_column_name = chinese_column_name)

def table_info(datatable_code):
    """查詢表格設定
    """
    from .connection import Connection
    import datetime

    path="datatables/%s/metadata" % datatable_code
    
    r = Connection.request('get', path).json()
    
    if 'datatable' in r:
        r=r['datatable']
        
        if r['status']['refreshed_at']:
            try:
                r['status']['refreshed_at']=datetime.datetime.strptime(r['status']['refreshed_at'],"%Y-%m-%dT%H:%M:%SZ")
            except:
                pass
            
        cols = {}
        for col in r['columns']:
            cols[col['name']]=col
            
        r['columns']=cols
    
    return r

def table_list():
    """取出所有可以使用的表格
    """
    from tejapi.connection import Connection
    path = "info/tables/list"
    r = Connection.request('get', path).json()
    return r['result']

def database_list():
    """取出所有可以使用的資料庫
    """
    from tejapi.connection import Connection
    path = "info/database/list"
    r = Connection.request('get', path).json()
    return r['result']

def category_list():
    """表格分類說明
    """
    from tejapi.connection import Connection
    path = "info/category/list"
    r = Connection.request('get', path).json()
    return r['result']
