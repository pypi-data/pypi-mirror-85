#! /usr/bin/env python3
# Copyright (c) 2018-2020 FASTEN.
#
# This file is part of FASTEN
# (see https://www.fasten-project.eu/).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import datetime
import json
from time import sleep
from abc import abstractmethod
from fasten.plugins.base import FastenPlugin
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


class KafkaPlugin(FastenPlugin):
    """Base interface for Kafka FASTEN plugins.
    """

    def __init__(self, bootstrap_servers):
        """Override this method to set Kafka Topics, consumer, and group_id
        """
        super().__init__()
        self.bootstrap_servers = bootstrap_servers
        self.consume_topic = None
        self.produce_topic = None
        self.log_topic = None
        self.error_topic = None
        self.group_id = None
        self.consumer = None
        self.producer = None

    @abstractmethod
    def consume(self, record):
        """Process an incoming record.

        Args:
            record (dict): message.value from a Kafka message, usually a dict.
        """

    def set_consumer(self):
        """Set consumer to read from consume_topic.
        """
        try:
            assert self.consume_topic is not None
            assert self.bootstrap_servers is not None
            assert self.group_id is not None
        except (AssertionError, NameError) as e:
            self.err(("You should have set consume_topic, bootstrap_servers, "
                      "and group_id"))
            raise e
        self.consumer = KafkaConsumer(
            self.consume_topic,
            bootstrap_servers=self.bootstrap_servers.split(','),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            max_poll_records=1,
            group_id=self.group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def set_producer(self):
        """Set producer to sent messages to produce_topic.
        """
        try:
            assert self.produce_topic is not None
            assert self.bootstrap_servers is not None
        except (AssertionError, NameError) as e:
            self.err("You should have set produce_topic, bootstrap_servers, ")
            raise e
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers.split(','),
            value_serializer=lambda x: x.encode('utf-8')
        )

    def create_message(self, input_message, extra):
        """Create a message to sent to a Kafka topic.

        Args:
            extra (dict): Should be a dict with payload or error as key.

        Returns:
            JSON message (dict)
        """
        message = {
            "plugin_name": self.name(),
            "plugin_version": self.version(),
            "input": input_message,
            "created_at": str(datetime.datetime.now().timestamp())
        }
        message.update(extra)
        return message

    def emit_message(self, topic, msg, phase, log_msg):
        """Send message to Kafka topic.

        Args:
            producer (KafkaProducer): Kafka producer to be used.
            topic (str): Kafka topic to send the messgae.
            msg (dict): Message to be sent.
            phase (str):) Phase.
            log_msg (str): Log message.
        """
        self.log("{}: Phase: {} Sent: {} to {}".format(
            str(datetime.datetime.now()), phase, log_msg, topic
        ))
        self.producer.send(topic, json.dumps(msg))

    def consume_messages(self):
        """Consume messages for consumer.
        """
        if self.consumer is None:
            raise NotImplementedError(
                "Use set_consumer before using handle_consume")
        for message in self.consumer:
            self.consumer.commit()
            record = message.value
            self.log("{}: Consuming: {}".format(
                str(datetime.datetime.now()), record))
            self.consume(record)

    def skip_messages(self):
        """Skip kafka messages
        """
        try:
            assert self.consumer is not None
        except (AssertionError, NameError) as e:
            self.err(("Consumer needs to be set before messages it can be "
                      "consumed."))
            raise e
        for _ in self.consumer:
            self.consumer.commit()

    def free_resource(self):
        """Free consumer and producer resources
        """
        try:
            if self.consumer is not None:
                self.consumer.close()
            if self.producer is not None:
                self.producer.close()
        except BaseException as e:
            self.err('Fatal exception while freeing resources: ' + str(e))
            raise e
        else:
            self.log('Resources freed successfully.')


class KafkaPluginNonBlocking(KafkaPlugin):

    def __init__(self, bootstrap_servers):
        """Override this method to set Kafka Topics, consumer, and group_id
        """
        super().__init__(bootstrap_servers)
        self.consumer_timeout_ms = None
        self.consumption_delay_sec = None

    def set_consumer_timeout_ms(self, consumer_timeout_ms):
        """Set consumer_timeout_ms
        """
        self.consumer_timeout_ms = consumer_timeout_ms

    def set_consumption_delay_sec(self, consumption_delay_sec):
        """Set consumption_delay_sec
        """
        self.consumption_delay_sec = consumption_delay_sec

    def set_consumer(self):
        """Set consumer to read (non-blocking) from consume_topic.
        """
        try:
            assert self.consume_topic is not None
            assert self.bootstrap_servers is not None
            assert self.group_id is not None
            assert self.consumer_timeout_ms is not None
        except (AssertionError, NameError) as e:
            self.err(("You should have set consume_topic, bootstrap_servers, "
                      "group_id, and consumer_timeout_ms"))
            raise e
        self.consumer = KafkaConsumer(
            self.consume_topic,
            bootstrap_servers=self.bootstrap_servers.split(','),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            max_poll_records=1,
            group_id=self.group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=self.consumer_timeout_ms
        )

    def set_consumer_with_retry(self):
        while True:
            try:
                self.set_consumer()
                self.set_producer()
            except NoBrokersAvailable:
                self.err("Could not connect consumer to Kafka, re-trying...")
            else:
                self.log("Connected consumer to Kafka successfully.")
                break
            sleep(self.consumption_delay_sec)

    def set_producer_with_retry(self):
        while True:
            try:
                self.set_producer()
            except NoBrokersAvailable:
                self.err("Could not connect producer to Kafka, re-trying...")
            else:
                self.log("Connected producer to Kafka successfully.")
                break
            sleep(self.consumption_delay_sec)
