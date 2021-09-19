![Lint](https://github.com/sdwilsh/brultest-serial2mqtt/workflows/Lint/badge.svg)
![Test](https://github.com/sdwilsh/brultest-serial2mqtt/workflows/Test/badge.svg)

# What is brultech-serial2mqtt?

This library talks to devices from [Brultech Research](https://www.brultech.com/)
over their serial port, using
[siobrultech-protocols](https://github.com/sdwilsh/siobrultech-protocols) to
decode the data, and then sends the data to an MQTT server.

## Development

### Setup

```
python3.9 -m venv .venv
source .venv/bin/activate

# Install Requirements
pip install -r requirements.txt

# Install Dev Requirements
pip install -r requirements-dev.txt

# One-Time Install of Commit Hooks
pre-commit install
```

### Testing

Tests are run with `pytest`.
