FROM python:alpine
  RUN git clone https://github.com/tagabenz/xbet.git
  WORKDIR xbet
  RUN apt install python3-pip -y
  RUN pip install -r requirements.txt
  CMD ["python3","start.py"]
