# From python3.6.15 base image
FROM python:3.6.15

# Set current working directory
WORKDIR /aiship_webapp

# Copy requirements file first to the working directory
COPY ./requirements.txt /aiship_webapp/requirements.txt

# Install package dependencies
RUN pip install --no-cache-dir --upgrade -r /aiship_webapp/requirements.txt

# copy files and directory to the working directory
COPY ./src/app /aiship_webapp/src/app/
COPY ./src/model /aiship_webapp/src/model/
COPY ./src/static /aiship_webapp/src/static/
COPY ./src/templates /aiship_webapp/src/templates/

# run uvicorn server
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80"]