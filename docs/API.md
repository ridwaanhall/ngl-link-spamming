# API Documentation

## NGL Link Spammer API Reference

### Core Classes

#### RequestSender

The main class for sending requests to NGL.link API.

```python
from ngl_spammer.core.request_sender import RequestSender

sender = RequestSender()
response = sender.send_request_with_retry(
    username="target_user",
    question="Hello!",
    device_id="device-id-here",
    game_slug="confessions"
)
```

**Methods:**

- `send_request()` - Send a single request
- `send_request_with_retry()` - Send request with retry logic
- `send_bulk_requests()` - Send multiple requests with delays

#### Generators

##### DeviceIDGenerator

Generates device IDs for requests.

```python
from ngl_spammer.generators.device_generator import DeviceIDGenerator

device_id = DeviceIDGenerator.generate()
```

##### MessageGenerator

Generates messages for requests.

```python
from ngl_spammer.generators.message_generator import MessageGenerator, MessageType

generator = MessageGenerator()
message = generator.generate(MessageType.HACKER)
```

##### GameSlugGenerator

Generates game slugs for NGL games.

```python
from ngl_spammer.generators.game_slug_generator import GameSlugGenerator

generator = GameSlugGenerator()
slug = generator.generate()
```

##### UserRegionGenerator

Maps country codes to country names.

```python
from ngl_spammer.generators.region_generator import UserRegionGenerator

country = UserRegionGenerator.get_country_name("US")  # "United States"
```

### Configuration

Configuration is managed through environment variables and the `config` module:

```python
from ngl_spammer.utils.config import config

# Access configuration values
print(config.ngl_api_url)
print(config.default_delay)
```

### Logging

Use the built-in logger for consistent logging:

```python
from ngl_spammer.utils.logger import logger

logger.info("This is an info message")
logger.error("This is an error message")
```

### CLI Interface

The CLI interface provides an easy way to interact with the tool:

```python
from ngl_spammer.cli.interface import CLIInterface

cli = CLIInterface()
cli.run()
```
