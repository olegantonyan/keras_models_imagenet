FROM ubuntu:17.10

ENV LANG=C.UTF-8 \
    LC_ALL=$LANG \
    FLASK_ENVIROMENT=production

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip && pip3 install pipenv && pipenv install

# download keras models upfront
RUN pipenv run python3 -c "from keras.applications.resnet50 import ResNet50; ResNet50(weights='imagenet')"

ENTRYPOINT ["pipenv", "run", "python3", "main.py"]

EXPOSE 5000
