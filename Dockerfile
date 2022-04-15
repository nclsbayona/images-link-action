FROM python:3

ADD Tree.py /Tree.py

ADD requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip wheel setuptools

RUN pip install --no-cache-dir -r requirements.txt

ADD main.py /main.py

RUN chmod +x /main.py

ENTRYPOINT [ "python", "/main.py" ]
