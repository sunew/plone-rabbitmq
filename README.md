#plone-rabbitmq

Setup of plone and collective.zamqp with rabbitmq


## Logging

Enable logging:

    environment-vars =
        ZAMQP_LOGLEVEL INFO


##  Effect of 

    zope-conf-additional =
        %import collective.zamqp

        <amqp-broker-connection>
            connection_id testrabbit
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


## test via commandline
Use the script publishmsg:

./bin/publishmsg -o localhost -u guest -p guest -v / -m testmessage -e testexchange -r newtestqueue

Works even when we cant connect via Zope


