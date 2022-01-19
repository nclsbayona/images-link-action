FROM python:3

ADD main.py /main.py

ADD Tree.py /Tree.py

ADD requirements.txt /requirements.txt

RUN chmod +x /main.py

RUN python -m pip install --upgrade pip wheel setuptools

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "/main.py" ]
