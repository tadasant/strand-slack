FROM python:3.6
MAINTAINER SolutionLoft
RUN mkdir -p /opt/code
WORKDIR /opt/code

# Copy just requirements.txt for caching. If the file hasn't changed
# then the RUN command that follows will not need to be re-run.
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt

COPY . .
WORKDIR /opt/code/
