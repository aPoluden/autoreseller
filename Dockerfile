# Use an official Python runtime as a parent image
FROM python:3.6

RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
#ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
ADD requirements.txt /app
RUN pip install -r requirements.txt

# Create non-privileged user (celery refuses to run under root)
RUN useradd -ms /bin/bash autoreseller
ADD . /app/

RUN chmod +x docker-entrypoint.sh
RUN chmod +x run_beat.sh
RUN chmod +x run_worker.sh

# Django needs full access to /static folder
# in case of /static folder exists
RUN rm -fr /app/static
RUN mkdir /app/static
RUN chown autoreseller:autoreseller -R /app/static
RUN chown autoreseller:autoreseller -R /app
RUN mkdir /var/autoreseller
RUN chown autoreseller:autoreseller -R /var/autoreseller

USER autoreseller

# If something changes IN this FILE  rebuild !!!