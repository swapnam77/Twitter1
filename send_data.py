from kafka import KafkaProducer
from random import randint
from time import sleep
import sys
import pickle
import os

BROKER = os.getenv('BROKER', 'localhost:9092')
TOPIC = 'tweets'

WORD_FILE='models/words'
WORDS = open(WORD_FILE).read().splitlines()

try:
    p=KafkaProducer(bootstrap_servers=BROKER)
except Exception as e:
    print(f"ERROR -->{e}")
    sys.exit(1)

dd = pickle.load(open("models/X_valid.sav", 'rb'))

for item in dd.to_numpy{}:
    p.send(TOPIC,bytes(str(item), encoding="utf8"))
    sleep(randint(1,4))
    