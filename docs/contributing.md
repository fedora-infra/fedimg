Fedimg welcomes contributors of all levels. Still, it can be a tricky project
to jump into because of its relative youth and the challenge of testing a
project that utilizes 3rd party services like AWS. This document hopes to
alleviate confusion and encourage potential contributors.

## Communicating with other contributors

Communication with other contributors is crucial. The best way to discuss
Fedimg development is by joining `#fedora-cloud` or `#fedora-apps` on the
Freenode IRC network. Alternatively, email can be sent to dgay@redhat.com. For
questions about the Fedora Infrastructure machines on which Fedimg runs, or
about related Fedmsgs, your best bet is to say something in `#fedora-apps`.

## Submitting changes

Fedimg is used with Git and hosted on
[GitHub](https://github.com/fedora-infra/fedimg). If you've managed to improve
Fedimg in some way, make sure to [file a pull
request](https://github.com/fedora-infra/fedimg/pulls), send in a patch via
email, or at least contact us via IRC. Emails can be sent to dgay@redhat.com.
IRC inquries should be sent to `oddshocks` in `#fedora-cloud` or `#fedora-apps`
on the Freenode network.

## Contributing code

Adding features and tackling
[issues](https://github.com/fedora-infra/fedimg/issues) via code changes are an
often-straightforward way to contribute. You can deploy your own instance of Fedimg
on your own machine to test your changes before sending them out to the world
(see [installation](/installation/) and [configuration](/configuration/)).

## Writing documentation

In some cases, it may be helpful to contribute some information of your own to
this documentation. For example, if you've found a way to make Fedimg work
on a special way to suit your particular needs, documenting your process
can greatly help others who find themselves in your same position.

Documentation can be added in
[Markdown](http://daringfireball.net/projects/markdown/syntax) to the [docs
directory](https://github.com/fedora-infra/fedimg/tree/develop/docs). Changes
should be submitted via a [pull
request](https://github.com/fedora-infra/fedimg/pulls).

## Fedimg on the Fedora infrastructure

Two machines on the Fedora infrastructure are devoted to Fedimg: fedimg01
(production) and fedimg01.stg (staging). As one might expect, fedimg01.stg
listens to the staging instance of Koji, and fedimg01 listens to production
Koji. These machines are managed via Ansible. The repo with our Ansible
configuration is
[here](https://infrastructure.fedoraproject.org/cgit/ansible.git).
