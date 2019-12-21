FROM ubuntu 

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

WORKDIR /home
ADD robocop.py .
ADD robocop robocop
ADD requirements.txt .
ADD .env .
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "robocop.py"]
