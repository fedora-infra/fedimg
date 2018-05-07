==============
FedimgConsumer
==============

Fedimg at it's core uses FedimgConsumer which is a Fedmsg consumer.
FedimgConsumer listions to the fedmsg bus for the completed `Pungi`_ composes.

FedimgConsumer listens to ``pungi.compose.status.change`` topic. On receiving a
message from fedmsg it:

- Checks if the `status` of the compose is either ``FINISHED_INCOMPLETE`` or
  ``FINISHED``.
- Then, it proceeds to strips the fedmsg-blanket to get the core message.
- It parses the image location and starts the upload process.
- For every event, Fedimg sends out a fedimg notification with the ``fedimg``
  category. Read more about the `list of topics here`_

.. _Pungi: https://pagure.io/pungi
.. _list of topics here: http://fedora-fedmsg.readthedocs.io/en/latest/topics.html#fedimg
