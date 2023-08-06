fasten-python-plugins
=====================

This package provides a template for creating FASTEN plug-ins.
It composed of two abstract classes; `FastenPlugin` and `KafkaPlugin`.
`FastenPlugin` implements logging methods `err` and `log`, and specifies
abstract methods abstract methods for declaring the metadata of a FASTEN
plug-in. `KafkaPlugin` implements the methods `set_consumer`, `set_producer`,
`create_message`, `emit_message`, and `consume_messages`. It also declares
the abstract method `consumes`.
An example is provided in the `demo` directory.

Install
-------

```
pip install fasten
```

Usage
-----

```python
from fasten.plugins.kafka import KafkaPlugin
```
