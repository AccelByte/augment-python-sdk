# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

FROM python:3.8.2-alpine3.11

# upgrade pip to use the latest one
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

WORKDIR /workspace
COPY . /workspace