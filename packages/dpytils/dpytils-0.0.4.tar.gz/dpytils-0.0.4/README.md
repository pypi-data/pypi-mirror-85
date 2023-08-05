# dpytils

## What is this?

It is a package with basic utilities for a discord bot main in discord.py.

## How do I use it?

To use it, simply import it, and initialize the `dpytils.utils()` class.

```python
from dpytils import utils
utilities = utils()
```

## What utilities are there?

Currently, only two. `randcolor()` and `permsfromvalue()`.

### randcolor

This function will return a random color (of type int) to be used for a discord embed, or anything else.

### permsfromvalue

This function will return another class, discordPermissions, which contains the following values.

#### permsfromvalue.perms_raw

The raw discord permissions object from [discord.py](https://github.com/Rapptz/discord.py).

#### permsfromvalue.perms_true

A list of permission names that are `True` from the given value

#### permsfromvalue.perms_false

A list of permission names that are `False` from the given value

#### permsfromvalue.perms_nice

A nicely formatted string with a list of permissions, and emoji to show true/false.
