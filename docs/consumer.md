Fedimg makes use of a Fedmsg consumer that listens to the Fedmsg bus for
completed Koji builds. It only cares about completed tasks of the method
`createImage`. The filtering process works like this:

1.  `KojiConsumer` (defined in `fedimg/consumers.py`) listens for Fedmsgs
    of the topic `org.fedoraproject.prod.buildsys.task.state.change`.

2.  If the message is of the `image` method, Fedimg looks at its children.

3.  If one of the message's children is of the `createImage` method, Fedimg
    checks that child's state.

4.  If the state is `2` (completed), the Fedmsg ID of that `createImage`
    task is passed to the Fedimg uploader, defined in `fedimg/uploader.py`.

## The fedmsg.d file

In order for Fedmsg to make use of Fedimg's `KojiConsumer`, the file found at
`fedmsg.d/fedimg.py` must have been copied into `/etc/fedmsg.d/`. The correct
Fedmsg endpoints must be configured as well, whether they are added to the
default list found in `fedmsg.d/fedimg.py` or if they are added by some Ansible
role or the like. We at the Fedora Infrastructure team make use of Ansible to
ensure that Fedmsg consumers in both staging and production are given the
necessary endpoints for their environment.
