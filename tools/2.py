#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 13:48
# @Author  : luozhenjie
# @FileName: 2.py
# @Software: PyCharm
import random,time

from paho.mqtt import client as mqtt_c
from locust import TaskSet,task,User,constant_pacing

broker_add = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt_topic_for_python"

client_id = f"python-mqtt-{random.randint(0,100)}"

def connect_mqtt():
    def on_connect(client,userdata,flags,rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n",rc)

    client = mqtt_c.Client(client_id)
    client.on_connect= on_connect
    client.connect(broker_add,port)

    return client

def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        msg = f"message: {msg_count}"
        result = client.publish(topic,msg)
        status = result[0]
        if status == 0:
            print(f"send `{msg}` to topic `{topic}` ")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


class TheTaskSet(TaskSet):
    @task
    def task_1(self):
        run()


class TheUser(User):
    tasks = [TheTaskSet]
    wait_time = constant_pacing(1)
