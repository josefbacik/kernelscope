FROM qnib/u-supervisor

RUN apt-get update
RUN apt-get install -y sqlite python3 python-pip gcc 
RUN apt-get install -y apt-transport-https
RUN apt-get install -y libmysqlclient-dev \
 && pip install mysql

ADD . /opt/kernelscope/
RUN cat /opt/kernelscope/kernelscope-sqlite.sql | sqlite3 /var/lib/kernelscope.db  
ADD etc/supervisord.d/kernelscope-visualiser.ini \
    etc/supervisord.d/kernelscope.ini \
    etc/supervisord.d/kernelscope-offcputime.ini \
    /etc/supervisord.d/
RUN echo "deb [trusted=yes] http://repo.iovisor.org/apt/xenial xenial-nightly main" > /etc/apt/sources.list.d/iovisor.list \
 && apt-get update -y \
 && apt-get install -y libelf1 \
 && apt-get install -y bcc-tools libbcc-examples
ADD entrypoint.sh /usr/bin/
CMD ["/usr/bin/entrypoint.sh", "/opt/qnib/supervisor/bin/start.sh", "-n"]

