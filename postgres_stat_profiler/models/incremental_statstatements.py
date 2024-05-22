

class incremental_statstatements:

    def __init__(self):
        self.create_tables = []
        self._getTableCreateCommands()
        self.create_indexes = []
        self._getIndexCreateCommands()
        self._getInsertQuery()
        
       
    def getCreateTables(self):
        return self.create_tables
    
    def getCreateIndexes(self):
        return self.create_indexes
    
    def getCollectQuery(self,name):
        self._getCollectQuery(name)
        return self.collectquery
    
    def getInsertQuery(self): 
        return self.insertquery
    
    def getInsertRecord(self,row):
        ir = {}
        ir['profilename'] = row['profilename']
        ir['result_time'] = row['result_time']
        ir['result_epoch'] = row['result_epoch']
        ir['username'] = row['username']
        ir['dbname'] = row['dbname']
        ir['dbid'] = row['dbid']
        ir['userid'] = row['userid']
        ir['querytype'] = row['querytype']
        ir['queryid'] = row['queryid']
        ir['query'] = row['query']
        ir['toplevel'] = row['toplevel']
        ir['calls'] = row['calls']
        ir['total_exec_time'] = row['total_exec_time']
        ir['min_exec_time'] = row['min_exec_time']
        ir['max_exec_time'] = row['max_exec_time']
        ir['mean_exec_time'] = row['mean_exec_time']
        ir['stddev_exec_time'] = row['stddev_exec_time']
        ir['rows'] = row['rows']
        ir['plans'] = row['plans']
        ir['total_plan_time'] = row['total_plan_time']
        ir['min_plan_time'] = row['min_plan_time']
        ir['max_plan_time'] = row['max_plan_time']
        ir['stddev_plan_time'] = row['stddev_plan_time']
        ir['shared_blks_hit'] = row['shared_blks_hit']
        ir['shared_blks_read'] = row['shared_blks_read']
        ir['shared_blks_dirtied'] = row['shared_blks_dirtied']
        ir['shared_blks_written'] = row['shared_blks_written']
        ir['local_blks_hit'] = row['local_blks_hit']
        ir['local_blks_read'] = row['local_blks_read']
        ir['local_blks_dirtied'] = row['local_blks_dirtied']
        ir['local_blks_written'] = row['local_blks_written']
        ir['temp_blks_read'] = row['temp_blks_read']
        ir['temp_blks_written'] = row['temp_blks_written']
        ir['blk_read_time'] = row['blk_read_time']
        ir['blk_write_time'] = row['blk_write_time']
        ir['wal_bytes'] = row['wal_bytes']
        ir['wal_records'] = row['wal_records']
        ir['wal_fpi'] = row['wal_fpi']
        irlist = list(ir.values())
        return irlist

    def _getTableCreateCommands(self):
        drop = \
        u"DROP TABLE postgres_stat_profiler.incremental_result_pg_stat_statements"
        self.create_tables.append(drop)
                
        create = \
        u"""CREATE TABLE postgres_stat_profiler.incremental_result_pg_stat_statements (
                profilename text,
                result_time timestamp,
                result_epoch bigint,
                username text,
                dbname text,
                dbid oid,
                userid oid,
                querytype text,
                queryid text,
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
        self.create_tables.append(create)

    def _getIndexCreateCommands(self):
        pass

    def _getCollectQuery(self,name):
        self.collectquery = """
        SELECT 
        latest.profilename as profilename,
        latest.result_time as result_time,
        latest.result_epoch as result_epoch,
        latest.username as username,
        latest.dbname as dbname,
	    latest.dbid as dbid,
	    latest.userid as userid,
        latest.querytype as querytype,
	    latest.queryid as queryid,
        latest.query as query,
        latest.toplevel as toplevel,
        latest.calls-previous.calls as calls,
        latest.total_exec_time-previous.total_exec_time as total_exec_time,
        CASE WHEN latest.calls-previous.calls = 0 THEN 0.0 ELSE latest.min_exec_time END as min_exec_time,
        CASE WHEN latest.calls-previous.calls = 0 THEN 0.0 ELSE latest.max_exec_time END as max_exec_time,
        CASE WHEN latest.calls-previous.calls = 0 THEN 0.0 ELSE (latest.total_exec_time-previous.total_exec_time)/(latest.calls-previous.calls) END as mean_exec_time,
        latest.stddev_exec_time as stddev_exec_time,
        latest.rows-previous.rows as rows,
        latest.plans-previous.plans as plans,
        latest.total_plan_time-previous.total_plan_time as total_plan_time,
        latest.min_plan_time as min_plan_time,
        latest.max_plan_time as max_plan_time,
        latest.stddev_plan_time as stddev_plan_time,
        latest.shared_blks_hit-previous.shared_blks_hit as shared_blks_hit,
        latest.shared_blks_read-previous.shared_blks_read as shared_blks_read,
        latest.shared_blks_dirtied-previous.shared_blks_dirtied as shared_blks_dirtied,
        latest.shared_blks_written-previous.shared_blks_written as shared_blks_written,
        latest.local_blks_hit-previous.local_blks_hit as local_blks_hit,
        latest.local_blks_read-previous.local_blks_read as local_blks_read,
        latest.local_blks_dirtied-previous.local_blks_dirtied as local_blks_dirtied,
        latest.local_blks_written-previous.local_blks_written as local_blks_written,
        latest.temp_blks_read-previous.temp_blks_read as temp_blks_read,
        latest.temp_blks_written-previous.temp_blks_written as temp_blks_written,
        latest.blk_read_time-previous.blk_read_time as blk_read_time,
        latest.blk_write_time-previous.blk_write_time as blk_write_time,
        latest.wal_bytes-previous.wal_bytes as wal_bytes,
        latest.wal_records-previous.wal_records as wal_records,
        latest.wal_fpi-previous.wal_fpi as wal_fpi
	    FROM
        (select * from postgres_stat_profiler.cumulative_result_pg_stat_statements where result_epoch in 
        (select max(result_epoch) from postgres_stat_profiler.cumulative_result_pg_stat_statements)) latest,
        (select * from postgres_stat_profiler.cumulative_result_pg_stat_statements where result_epoch in 
        (select max(result_epoch)-60 from postgres_stat_profiler.cumulative_result_pg_stat_statements)) previous
        where latest.profilename = '{}' and 
        (previous.userid = latest.userid and previous.dbid = latest.dbid and previous.queryid = latest.queryid)
        """.format(name)

    def _getInsertQuery(self):
         self.insertquery = """
        INSERT into postgres_stat_profiler.incremental_result_pg_stat_statements (
                profilename,
                result_time,
                result_epoch,
                username,
                dbname,
                dbid,
                userid,
                querytype,
                queryid,
                query,
                toplevel,
                calls,
                total_exec_time,
                min_exec_time,
                max_exec_time,
                mean_exec_time,
                stddev_exec_time,
                rows,
                plans,
                total_plan_time,
                min_plan_time,
                max_plan_time,
                stddev_plan_time,
                shared_blks_hit,
                shared_blks_read,
                shared_blks_dirtied,
                shared_blks_written,
                local_blks_hit,
                local_blks_read,
                local_blks_dirtied,
                local_blks_written,
                temp_blks_read,
                temp_blks_written,
                blk_read_time,
                blk_write_time,
                wal_bytes,
                wal_records,
                wal_fpi
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s
            )
        """
