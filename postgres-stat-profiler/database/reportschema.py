

class reportschema():

    def __init__(self):
        self.create_tables = []
        self.create_indexes = []
        self._getTableCommands()
        self._getIndexCommands()
    
    def getCreateTables(self):
        return self.create_tables
    
    def getTestCommand(self):
        return u'SELECT * FROM cumulative_result_pg_stat_statements LIMIT 1'

    def _getTableCommands(self):
        drop_cumulative_result_pg_stat_statements = \
        u"DROP TABLE cumulative_result_pg_stat_statements"
        self.create_tables.append(drop_cumulative_result_pg_stat_statements)
                
        cumulative_result_pg_stat_statements = \
        u"""
            CREATE TABLE cumulative_result_pg_stat_statements (
                profilename text,
                result_time timestamp,
                result_epoch bigint,
                dbname text,
                username text,
                dbid oid,
                userid oid,
                queryid bigint,
                query text,
                toplevel boolean,
                calls bigint,
                total_exec_time double precision,
                min_exec_time double precision,
                max_exec_time double precision,
                mean_exec_time double precision,
                stddev_exec_time double precision,
                rows bigint,
                plans bigint,
                total_plan_time double precision,
                min_plan_time double precision,
                max_plan_time double precision,
                stddev_plan_time double precision,
                shared_blks_hit bigint,
                shared_blks_read bigint,
                shared_blks_dirtied bigint,
                shared_blks_written bigint,
                local_blks_hit bigint,
                local_blks_read bigint,
                local_blks_dirtied bigint,
                local_blks_written bigint,
                temp_blks_read bigint,
                temp_blks_written bigint,
                blk_read_time double precision,
                blk_write_time double precision,
                wal_bytes numeric,
                wal_records bigint,
                wal_fpi bigint
            )
        """
        self.create_tables.append(cumulative_result_pg_stat_statements)

    def _getIndexCommands(self):
        pass
