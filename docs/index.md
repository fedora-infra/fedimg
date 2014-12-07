# Fedimg

Fedimg is a service that automatically uploads completed Fedora image builds to
internal and external cloud services. By listening to the
[Fedmsg](http://www.fedmsg.com/en/latest/) hub for
[Koji](http://koji.fedoraproject.org/koji/) build messages, Fedimg is able to
make newly built Fedora images available for testing and use through a number
of cloud service providers, such as Amazon Web Services.

Fedimg was written by David Gay, with contributions from Ralph Bean.

## License

Fedimg is licensed under the AGPL, version 3 or later. See the source code for
the [full license
text](https://github.com/fedora-infra/fedimg/blob/develop/LICENSE).
