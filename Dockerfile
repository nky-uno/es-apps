FROM python:3.7.4
RUN pip install --upgrade pip
 
ARG project_directory
WORKDIR $project_directory

COPY pymodules/ /pymodules
ENV PYTHONPATH "${PYTONPATH}:/pymodules"
 
RUN pip install retry flask pandas elasticsearch elasticsearch_dsl dash dash-bootstrap-components
