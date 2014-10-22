#plone-rabbitmq

Setup of plone and collective.zamqp with rabbitmq


## Logging

Enable logging, you can't work with your eyes shut:

    environment-vars =
        ZAMQP_LOGLEVEL INFO


##  Setup a connection

    zope-conf-additional =
        %import collective.zamqp

        <amqp-broker-connection>
            connection_id testrabbit
            keepalive 60
            heartbeat 60
        </amqp-broker-connection>

What happens on the RabbitMQ side?

On zope startup:
- a connection shows up in the rabbit mq management interface
- a channel for the connection
- And: a durable exchange with the name of the connection_id 

Log:

    2014-10-22 13:45:27 INFO Zope Ready to handle requests
    2014-10-22 13:45:27 INFO collective.zamqp Producer ready to publish to exchange '' with routing key '' on connection 'testrabbit'
    2014-10-22 13:45:27 INFO collective.zamqp Producer declared exchange 'testrabbit' on connection 'testrabbit'
    2014-10-22 13:45:27 INFO collective.zamqp Producer ready to publish to exchange 'testrabbit' with routing key 'testrabbit.testqueue' on connection 'testrabbit'

## sending a message - with no consumer
If there is no queue, the message is lost.

And the queue was in my case only set up by the consumer. By default the producer only sets the routing key and the exchange, not the queue.

## Setup a consumer
In this case in a seperate instance:

    [instance-worker]
    <= instance
    http-address = 8082

    zope-conf-additional =
        %import collective.zamqp

        <amqp-broker-connection>
            connection_id testrabbit
            keepalive 60
            heartbeat 60
        </amqp-broker-connection>

        <amqp-consuming-server>
            connection_id testrabbit
            site_id site
        </amqp-consuming-server>

Now the queue shows up in the rabbitmq interface. 

Sending / recieving works.

## Ack and durability
After recieving a message, send message.ack()

If not we get a warning: 

    2014-10-22 22:13:45 INFO collective.zamqp Received message '35' sent to exchange 'testrabbit' with routing key 'testrabbit.testqueue'
    2014-10-22 22:13:46 INFO collective.zamqp Worker started processing message '35' (status = 'RECEIVED', age = '0:00:00.301177')
    2014-10-22 22:13:46 INFO rabbitmqtest Processing message: 65216771A6pqc7X-jGY-1414008770.
    2014-10-22 22:13:46 WARNING collective.zamqp Nobody acknowledged or rejected message '35' sent to exchange exchange 'testrabbit' with routing key 'testrabbit.testqueue'

If not ack'ed, it will be requed and sent again (to another instance or to the same after restart.)

Durability for the message (delivery_mode = 2) is on per default if durable=True for the producer.

Durability for queue and exchange is on if durable=True for producer and/or consumer.

##

## Keepalive
set keepalive to a number of seconds.
The keepalive messages can be seen in the rabbitmq interface.
This can be seen in the Z2 log:

    127.0.0.1 - Anonymous [22/Oct/2014:21:23:56 +0200] "GET /testrabbit.ping HTTP/1.0" 204 0 "" "Zope Clock Server Client"
    127.0.0.1 - Anonymous [22/Oct/2014:21:24:26 +0200] "GET /testrabbit.ping HTTP/1.0" 204 0 "" "Zope Clock Server Client"
    ...

BUT: we need a consumer set up to get the pings.
Back to the producer instance?
Or is it enough with the dedicated worker instance?

## No connection problem
After zope startup, no connection is made to rabbitmq. No connection shows up in the rabbitmq interface.
Trying to send a message: 
    
    collective.zamqp No connection. Durable message was left into volatile memory to wait for a new connection

Restart rabbitmq, zope, zeo: still the same problem.

Uden sauna: så virker det.

## socket error problem
A timeout maybe (a long time spent in the debugger).
But it continues to happen even after the automatic reconnect.
A restart of zope is needed.

Happens after:

    2014-10-22 22:34:26 WARNING collective.zamqp Channel closed with reason '404 NOT_FOUND - no exchange 'collective.zamqp' in vhost '/''
    2014-10-22 22:34:26 INFO collective.zamqp Trying to reconnect connection 'testrabbit' in 1.0 seconds
    /work/buildout_cache/eggs/pika-0.9.5-py2.7.egg/pika/callback.py:69: UserWarning: CallbackManager.add: Duplicate callback found for "0:Connection.CloseOk"
      (self.__class__.__name__, prefix, key))
    2014-10-22 22:34:26 INFO pika Disconnected from RabbitMQ at localhost:5672
    2014-10-22 22:34:26 INFO pika Disconnected from RabbitMQ at localhost:5672
    2014-10-22 22:34:56 INFO collective.zamqp Connection 'testrabbit' connecting
    2014-10-22 22:35:26 ERROR ZServer uncaptured python exception, closing channel <collective.zamqp.connection.AsyncoreDispatcher localhost:5672 at 0x7f8508422a28> (<class 'socket.error'>:[Errno 104] Connection reset by peer [/usr/lib/python2.7/asyncore.py|read|83] [/usr/lib/python2.7/asyncore.py|handle_read_event|446] [/usr/lib/python2.7/asyncore.py|handle_connect_event|454])
    2014-10-22 22:42:04 INFO collective.zamqp Trying to reconnect connection 'testrabbit' in 1.48490881522 seconds
    2014-10-22 22:42:04 INFO pika Disconnected from RabbitMQ at localhost:5672
    2014-10-22 22:42:34 INFO collective.zamqp Connection 'testrabbit' connecting

And after a few retries it came back up.

Wonder why it closed with a 404 on the keepalive exchange. Is there, and came back up.

## stopping and starting rabbitmq
Running zope instances reconnect.


## test via commandline
Use the script publishmsg:

./bin/publishmsg -o localhost -u guest -p guest -v / -m testmessage -e testexchange -r newtestqueue

Works even when we cant connect via Zope


