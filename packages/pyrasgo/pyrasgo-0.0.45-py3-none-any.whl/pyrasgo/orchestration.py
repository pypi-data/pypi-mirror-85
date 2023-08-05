from pyrasgo.connection import Connection
from pyrasgo.monitoring import track_usage
from pyrasgo.rasgo import Rasgo

class RasgoOrchestration(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rasgo = Rasgo(api_key=self._api_key)

    @track_usage
    def simulate_orchestration(self, source_table: str, func):
        '''
        Run a python function against a source table
        
        param source_table: Snowflake table holding raw data
        param func: function containing feature transformation code (should be named generate_feature)

        return: Success or Failure message
        '''
        df = self.rasgo.get_source_table(table_name=source_table, record_limit=-1)
        dx = func(df)
        return f'Code successfully created dataframe with shape {dx.shape}'
