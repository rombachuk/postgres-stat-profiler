import psycopg
from datetime import datetime

class cumulative_statstatements:

    def __init__(self):
        self.create_tables = []
        self._getTableCreateCommands()
        self.create_indexes = []
        self._getIndexCreateCommands()
        self._getCollectQuery()
        self._getInsertQuery()
       
    def getCreateTables(self):
        return self.create_tables
    
    def getCreateIndexes(self):
        return self.create_indexes
    
    def getCollectQuery(self):
        return self.collectquery
    
    def getInsertQuery(self):
        return self.insertquery
    
    def getInsertRecord(self,name,recordtime,recordepoch,row):
        ir = {}
        ir['profilename'] = name
        ir['result_time'] = recordtime
        ir['result_epoch'] = recordepoch
        ir['username'] = row['username']
        ir['dbname'] = row['dbname']
        ir['dbid'] = row['dbid']
        ir['userid'] = row['userid']
        ir['querytype'] = u'temp'
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
        u"DROP TABLE postgres_stat_profiler.cumulative_result_pg_stat_statements"
        self.create_tables.append(drop)
                
        create = \
        u"""CREATE TABLE postgres_stat_profiler.cumulative_result_pg_stat_statements (
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

    def _getCollectQuery(self):
        self.collectquery = """
         SELECT 
                pu.usename as username,
                pd.datname as dbname,
                pss.dbid as dbid,
                pss.userid as userid,
                pss.queryid as queryid,
                pss.query as query,
                pss.toplevel as toplevel,
                pss.calls as calls,
                pss.total_exec_time as total_exec_time,
                pss.min_exec_time as min_exec_time,
                pss.max_exec_time as max_exec_time,
                pss.mean_exec_time as mean_exec_time,
                pss.stddev_exec_time as stddev_exec_time,
                pss.rows as rows,
                pss.plans as plans ,
                pss.total_plan_time as total_plan_time,
                pss.min_plan_time as min_plan_time,
                pss.max_plan_time as max_plan_time,
                pss.stddev_plan_time as stddev_plan_time,
                pss.shared_blks_hit as shared_blks_hit,
                pss.shared_blks_read as shared_blks_read,
                pss.shared_blks_dirtied as shared_blks_dirtied,
                pss.shared_blks_written as shared_blks_written,
                pss.local_blks_hit as local_blks_hit,
                pss.local_blks_read as local_blks_read,
                pss.local_blks_dirtied as local_blks_dirtied,
                pss.local_blks_written as local_blks_written, 
                pss.temp_blks_read as temp_blks_read,
                pss.temp_blks_written as temp_blks_written,
                pss.blk_read_time as blk_read_time,
                pss.blk_write_time as blk_write_time,
                pss.wal_bytes as wal_bytes,
                pss.wal_records as wal_records,
                pss.wal_fpi as wal_fpi
         from pg_stat_statements pss, pg_catalog.pg_user pu, pg_catalog.pg_database pd 
         WHERE pss.userid=pu.usesysid AND pss.dbid = pd.oid 
         order by total_exec_time desc limit 100
        """

    def _getInsertQuery(self):
        self.insertquery = """
        INSERT into postgres_stat_profiler.cumulative_result_pg_stat_statements (
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