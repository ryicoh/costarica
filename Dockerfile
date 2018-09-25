FROM alpine:3.8
LABEL maintainer="Ryuichiroh Ikeuchi <ryicoh@gmial.com>"

RUN apk update && \
    apk add --no-cache python3 \
                       python3-dev \
                       build-base \
                       postgresql-dev && \
    python3 -m ensurepip && \
    pip3 install pip setuptools -U

ADD . /costarica
WORKDIR /costarica
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]
