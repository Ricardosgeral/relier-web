FROM heroku/miniconda:3

# Grab requirements.txt.
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add the code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

#RUN conda install scikit-learn
RUN apt-get update && apt-get install -y \
    python3-pandas \

CMD gunicorn --bind 0.0.0.0:$PORT wsgi