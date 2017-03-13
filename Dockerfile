FROM qnib/u-supervisor

RUN echo "deb [trusted=yes] http://repo.iovisor.org/apt/xenial xenial-nightly main" > /etc/apt/sources.list.d/iovisor.list \
 && apt-get update \
 && apt-get install -y sqlite python3 python-pip gcc apt-transport-https libmysqlclient-dev libelf1 bcc-tools libbcc-examples \
 && pip install mysql

ADD . /opt/kernelscope/
RUN cat /opt/kernelscope/kernelscope-sqlite.sql | sqlite3 /var/lib/kernelscope.db  
ADD etc/supervisord.d/kernelscope-visualiser.ini \
    etc/supervisord.d/kernelscope.ini \
    etc/supervisord.d/kernelscope-offcputime.ini \
    /etc/supervisord.d/
ADD entrypoint.sh /usr/bin/
CMD ["/usr/bin/entrypoint.sh", "/opt/qnib/supervisor/bin/start.sh", "-n"]

