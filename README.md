#plone-rabbitmq

Setup of plone and collective.zamqp with rabbitmq


## Logging

    environment-vars =
        ZAMQP_LOGLEVEL DEBUG

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


## No connection problem
After zope startup, no connection is made to rabbitmq. No connection shows up in the rabbitmq interface.
Trying to send a message: 
    
    collective.zamqp No connection. Durable message was left into volatile memory to wait for a new connection

Restart rabbitmq, zope, zeo: still the same problem.
