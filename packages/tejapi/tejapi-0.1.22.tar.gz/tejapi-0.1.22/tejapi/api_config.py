class ApiConfig:
    api_key = None
    api_base = 'https://api.tej.com.tw'
    api_version = "1.0.0"
    page_limit = 100
    ignoretz = False
    
    @staticmethod
    def info():
        from tejapi.connection import Connection
        import datetime
        path="apiKeyInfo/%s" % ApiConfig.api_key
        r = Connection.request('get', path).json()
        r['startDate']=datetime.datetime.strptime(r['startDate'],'%Y-%m-%d').date()
        if(r['endDate'] != None):
            r['endDate']=datetime.datetime.strptime(r['endDate'],'%Y-%m-%d').date()
        return r