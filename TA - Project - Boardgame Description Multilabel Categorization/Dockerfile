# -*- dockerfile -*-
FROM ubuntu:latest

# Define Dockerfile arguments
# Note that ARGs are available at build time and can be specified with --build-arg VAR_NAME=VAR_VALUE at build time
# On the other hand you CANNOT override ENV during build time; but they will be available in the container
# as env variables, while the ARGs will NOT
ARG docker_api_dir=/api
ARG docker_models_dir=${docker_api_dir}/models
ARG docker_src_dir=${docker_api_dir}/src
ARG HTTP_PORT=5001

# Create Image file locations
RUN mkdir -p ${docker_api_dir} && mkdir -p ${docker_models_dir} && mkdir -p ${docker_src_dir}

# Installing necessary functionalities
RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc g++

# Copy the files in the root folder to the api folder inside the container
COPY ./api.py ${docker_api_dir}/api.py
COPY ./requirements.txt ${docker_api_dir}/requirements.txt
COPY ./api_entrypoint.sh ${docker_api_dir}/api_entrypoint.sh

# Add files from models to the models folder inside the container
# Add files from src to the src folder inside the container
ADD models ${docker_models_dir}
ADD src ${docker_src_dir}

# Move to api dir, upgrade pip and install requirements.txt
WORKDIR ${docker_api_dir}
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader stopwords

# Setting model location
ENV MODEL_FILE="${docker_models_dir}/linear_svc_ovr.pkl"
ENV TFIDF_VECTORIZER_FILE="${docker_models_dir}/tfidf_vectorizer.pkl"
ENV CATEGORIES_FILE="${docker_models_dir}/categories.pkl"

EXPOSE ${HTTP_PORT}
# Once it builds the image, execute the api_entrypoint.sh script
CMD ["sh", "api_entrypoint.sh"]