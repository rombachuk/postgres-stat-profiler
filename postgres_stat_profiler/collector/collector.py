import psycopg
from psycopg.rows import dict_row
import logging
from postgres_stat_profiler.collector.monitoredDatabase import monitoredDatabase
from postgres_stat_profiler.collector.reportDatabase import reportDatabase
from postgres_stat_profiler.models.cumulative_statstatements import cumulative_statstatements
from postgres_stat_profiler.models.incremental_statstatements import incremental_statstatements

class collector:

    def __init__(self,name, monitorconn,reportconn):
        self.profilename = name
        self.monitor_connection = monitorconn
        self.monitordb = monitoredDatabase(self.monitor_connection.getConnectionString())
        self.report_connection =  reportconn
        self.reportdb = reportDatabase(self.report_connection.getConnectionString())

    def getMonitoredDBstatus(self):
        return self.monitordb.getStatus()

    def getReportDBstatus(self):
        return self.reportdb.getStatus()

    def collect(self):
        if self.monitordb.getStatus() == u'operational' \
        and self.reportdb.getStatus() == u'initialised':
            try:
               cumulativess = cumulative_statstatements()
               cumulative_collectquery = cumulativess.getCollectQuery()

               mconn = psycopg.connect(self.monitordb.getConnstring(),row_factory=dict_row)
               collectrecords = mconn.execute(cumulative_collectquery).fetchall()
               rowcount = 0
               for collectrecord in collectrecords:
                   cumulative_insertquery = cumulativess.getInsertQuery()
                   insert_record = cumulativess.getInsertRecord(self.profilename,collectrecord)
                   result = mconn.execute(cumulative_insertquery, insert_record)
                   rowcount = rowcount+1

            except (Exception, psycopg.Error) as e:
               logging.warning('pg-stat-profiler: collector : query error [{}]'.format(str(e)))