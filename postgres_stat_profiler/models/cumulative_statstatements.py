import psycopg

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
    
    def getInsertRecord(self,name,row):
        ir = {}
        ir['profilename'] = name
        ir['result_time'] = None
        ir['result_epoch'] = None
        ir['dbname'] = row['dbname']
        ir['username'] = row['username']
        ir['dbid'] = row['dbid']
        ir['userid'] = row['userid']
        ir['username'] = row['username']
        ir['queryid'] = row['queryid']
        ir['query'] = row['query']
        ir['toplevel'] = row['toplevel']
        ir['calls'] = row['calls']
        ir['username'] = row['username']
        ir['username'] = row['username']
        


    def _getTableCreateCommands(self):
        drop = \
        u"DROP TABLE postgres_stat_profiler.cumulative_result_pg_stat_statements"
        self.create_tables.append(drop)
                
        create = \
        u"""CREATE TABLE postgres_stat_profiler.cumulative_result_pg_stat_statements (
                profilename text,
                result_time timestamp,
                result_epoch bigint,
                dbname text,
                username text,
                dbid oid,
                userid oid,
                querytype text,
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
        self.create_tables.append(create)

    def _getIndexCreateCommands(self):
        pass

    def _getCollectQuery(self):
        self.collectquery = """
         select usename,datname,queryid,left(query,100)as query_first_100chars,calls,
         round(total_exec_time::numeric,3) as total_exec_time,round(mean_exec_time::numeric,3) as mean_exec_time 
         from pg_stat_statements pss, pg_catalog.pg_user pu, pg_catalog.pg_database pd 
         WHERE pss.userid=pu.usesysid AND pss.dbid = pd.oid 
         order by total_exec_time desc limit 100
        """

    def _getInsertQuery(self):
        self.insertquery = """
        INSERT into postgres_stat_profiler.cumulative_result_pg_stat_statements (
                profilename text,
                result_time timestamp,
                result_epoch bigint,
                dbname text,
                username text,
                dbid oid,
                userid oid,
                querytype text,
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
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s
            )
        """