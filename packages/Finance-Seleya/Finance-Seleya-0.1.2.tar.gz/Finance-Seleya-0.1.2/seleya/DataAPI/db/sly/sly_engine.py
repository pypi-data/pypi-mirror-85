from .. fetch_engine import FetchEngine
from .... config.default_config import DB_URL
from .... utilities.singleton import Singleton
from sqlalchemy import select, and_, outerjoin, join, column
import six,pdb
import numpy as np
import pandas as pd

@six.add_metaclass(Singleton)
class FetchSLYEngine(FetchEngine):
    def __init__(self):
        super(FetchSLYEngine, self).__init__('sly', DB_URL['sly'])
    
    def show_cloumns(self, name):
        result = self._insp.get_columns(name)
        result = [r for r in result if r['name'] not in ['timestamp','flag']]
        return pd.DataFrame(result).drop(['default','comment','nullable','autoincrement'],axis=1)
      
    
    def default_multiple(self, table, key_name, key_value,
                        query_name, query_values):
        return and_(table.__dict__[key_name] == key_value,
                   table.flag == 1, table.__dict__[query_name].in_(query_values)
                   )
    def default_dates(self, table,  dates, 
                      time_name='trade_date', codes=None, key=None):
       
        return and_(table.__dict__[time_name].in_(dates),
                    table.flag == 1) if key is None else and_(table.__dict__[time_name].in_(dates),
                    table.flag == 1, table.__dict__[key].in_(codes)) 
    
    def default_notdates(self, table, begin_date, end_date, 
                         time_name='trade_date',
                         codes=None, key=None):
        return and_(table.__dict__[time_name] >= begin_date, 
                               table.__dict__[time_name] <= end_date,
                               table.flag == 1) if key is None else and_(table.__dict__[time_name] >= begin_date, 
                               table.__dict__[time_name] <= end_date,
                               table.flag == 1, table.__dict__[key].in_(codes))
    
    def gd_overview(self, codes, key=None, columns=None):
        table = self._base.classes['gd_overview']
        return self.base_notime(table=table, codes=codes, key=key, 
                                columns=columns, clause_list=None)
    
    def gd_reviews(self, codes=None, key=None, begin_date=None, end_date=None, 
               columns=None, freq=None, dates=None):
        table = self._base.classes['gd_reviews']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='reviewDateTime') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='reviewDateTime')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='reviewDateTime')
    
    def gdelt_feed(self, codes=None, key=None, begin_date=None, end_date=None, 
               columns=None, freq=None, dates=None):
        table = self._base.classes['gdelt_feed']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='publish_time') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='publish_time')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='publish_time')
    
    
    def gdelt_geo(self, codes=None, key=None, columns=None):
        table = self._base.classes['gdelt_geo']
        return self.base_notime(table=table, codes=codes, key=key, 
                                columns=columns, clause_list=None)
    
    def gdelt_timelinetone(self, codes=None, key=None, begin_date=None, end_date=None,
                          columns=None, freq=None, dates=None):
        table = self._base.classes['gdelt_timelinetone']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='date') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='date')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='date')
    
    def gdelt_timelinevolinfo(self, codes=None, key=None, begin_date=None, end_date=None,
                          columns=None, freq=None, dates=None):
        table = self._base.classes['gdelt_timelinevolinfo']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='date') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='date')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='date')
    
    def gdelt_timelinevolraw(self, codes=None, key=None, begin_date=None, end_date=None,
                          columns=None, freq=None, dates=None):
        table = self._base.classes['gdelt_timelinevolraw']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='date') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='date')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='date')
    
    def bhr_feed(self, codes=None, key=None, begin_date=None, end_date=None,
                          columns=None, freq=None, dates=None):
        table = self._base.classes['bhr_feed']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='publish_time') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='publish_time')
            
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='publish_time')
    
    def bhr_label(self, key_name, key_value, query_name, query_values, 
                  columns=None, freq=None):
        table = self._base.classes['bhr_label']
        clause_list = self.default_multiple(table, key_name, key_value,
                        query_name, query_values)
        return self.base_multiple(table=table, clause_list=clause_list, columns=None)
        
    def bd_label_data(self, codes=None, key=None, begin_date=None, end_date=None,
                          columns=None, freq=None, dates=None):
        table = self._base.classes['bd_label_data']
        if dates is not None:
            clause_list = self.default_dates(table=table, dates=dates, 
                                             codes=codes, key=key, 
                                             time_name='date') 
        else:
            clause_list = self.default_notdates(table=table, begin_date=begin_date, 
                                                end_date=end_date, codes=codes, key=key,
                                                time_name='date')
        return self.base(table=table, begin_date=begin_date, end_date=end_date, 
                         codes=codes, key=key, columns=columns, freq=freq, 
                         dates=dates, clause_list=clause_list,time_name='date')