FROM qnib/alpn-base

ADD . /opt/kernelscope/
RUN apk add --no-cache sqlite python3
RUN cat /opt/kernelscope/kernelscope-sqlite.sql | sqlite3 /var/lib/kernelscope.db
RUN apk --no-cache add py-pip mysql-dev gcc python-dev linux-headers musl-dev \
 && pip install mysql

CMD ["python", "/opt/kernelscope/src/KernelscopeLoggerService.py", "--sqlite", "kernelscope.db", "8081"]

