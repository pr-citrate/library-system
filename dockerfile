FROM node:19
FROM python:3.11
RUN python -m pip install pynecone
CMD pc run --env prod~