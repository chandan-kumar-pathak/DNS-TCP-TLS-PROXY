FROM python:3

 ADD dnsproxy.py /
 RUN pip install dnslib
 EXPOSE 9999/udp
 CMD [ "python", "./dnsproxy.py" ]
