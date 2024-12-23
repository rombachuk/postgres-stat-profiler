from postgres_stat_profiler.models.cumulative_statstatements import cumulative_statstatements
from postgres_stat_profiler.models.incremental_statstatements import incremental_statstatements

class reportschema():

    def __init__(self):
        self.create_schema = []
        self.create_tables = []
        self.create_indexes = []
        self._getSchemaCommands()
        self._getTableCommands()
        self._getIndexCommands()

    def getCreateSchema(self):
        return self.create_schema
    
    def getCreateTables(self):
        return self.create_tables
    
    def getCreateIndexes(self):
        return self.create_indexes
    
    def getTestCommand(self):
        return u'SELECT * FROM postgres_stat_profiler.cumulative_result_pg_stat_statements LIMIT 1'

    def _getSchemaCommands(self):
        drop_postgres_stat_profiler_schema = \
        u"DROP SCHEMA postgres_stat_profiler"
        self.create_schema.append(drop_postgres_stat_profiler_schema)

        create_postgres_stat_profiler_schema = \
        u"CREATE SCHEMA postgres_stat_profiler"
        self.create_schema.append(create_postgres_stat_profiler_schema)

    def _getTableCommands(self):
        cumulativess = cumulative_statstatements()
        incrementalss = incremental_statstatements()
        self.create_tables = cumulativess.getCreateTables() + incrementalss.getCreateTables()

    def _getIndexCommands(self):
        cumulativess = cumulative_statstatements()
        incrementalss = incremental_statstatements()
        self.create_indexes = cumulativess.getCreateIndexes() + incrementalss.getCreateIndexes()
