# Sublime RSpec toggle

Sublime Text package to easily switch between implementation and spec. It is originally based on https://github.com/fnando/sublime-better-rspec (which seems abandoned) and extended. This package only includes the code for the toggling command, no syntax/.. the original one included.

## Installation

This package is not on packagecontrol.io (yet?).

### Git Clone

Clone this repository into the Sublime Text “Packages” directory, which is located where ever the “Preferences” -> “Browse Packages” option in sublime takes you.

## Toggling between implementation/spec

The default binding is `super-period`.

```json
{
  "keys": ["super+period"],
  "command": "rspec_toggle"
}
```

You can change it to whatever you by adding the following snippet to your Keybindings file.

```json
{
  "keys": ["ctrl+alt+down"],
  "command": "rspec_toggle"
}
```
