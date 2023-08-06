# quiltz-domain

python domain concepts for quiltz

## Purpose

At QWAN we're building some applications in python. We collect usefull stuff in
quiltz packages:

* **quiltz-domain** (this package) contains domain level modules like, entity
  id's, results, an email anonymizer, validators and parsers
* [**quiltz-testsupport**](https://github.com/qwaneu/quiltz-testsupport) contains test support modules, that supports mainly non
  unit tests, like integrating with smtp, probing asynchronous results and
  asserting log statements
* [**quiltz-messaging**](https://github.com/qwaneu/quiltz-messaging) contains a
  messaging domain concept and an engines to send the messages. Currently only
  smtp sending is supported.

## installing 

```bash
pip install quitlz-domain
```

See [documentation](doc/index.md)
