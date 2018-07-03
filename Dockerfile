FROM heroku/miniconda:3

# Grab requirements.txt.
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -r /tmp/requirements.txt

# Add the code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

#install numpy and pandas using conda
RUN conda install numpy
RUN conda install pandas

#CMD gunicorn --bind 0.0.0.0:$PORT wsgi