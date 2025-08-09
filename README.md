# NGL Link Spammer v2.0.0

A professional, maintainable tool for sending anonymous messages to NGL.link with advanced features including rate limiting, adaptive delays, and IP rotation.

## ✨ Features

- 🏗️ **Professional Architecture** - Clean, modular, and maintainable code structure
- 🔄 **Adaptive Rate Limiting** - Intelligent delay management to avoid detection
- 🌐 **IP Rotation** - Header spoofing with realistic IP addresses
- 📊 **Real-time Statistics** - Progress tracking and success rate monitoring
- ⚙️ **Configurable Settings** - Environment-based configuration management
- 🧪 **Unit Testing** - Comprehensive test coverage
- 📚 **Documentation** - Complete API documentation and usage guides
- 🛡️ **Error Handling** - Robust error handling and retry mechanisms

## 📁 Project Structure

```txt
ngl-link-spamming/
├── src/ngl_spammer/           # Main package
│   ├── core/                  # Core functionality
│   │   └── request_sender.py  # Main request handling
│   ├── generators/            # Data generators
│   │   ├── device_generator.py
│   │   ├── message_generator.py
│   │   ├── game_slug_generator.py
│   │   └── region_generator.py
│   ├── utils/                 # Utilities
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging utilities
│   │   └── network.py         # Network utilities
│   └── cli/                   # Command-line interface
│       └── interface.py
├── scripts/                   # Entry point scripts
│   ├── custom.py
│   └── random.py
├── config/                    # Configuration files
│   └── .env.example
├── tests/                     # Unit tests
├── docs/                      # Documentation
└── requirements.txt
```

## 🚀 Installation

### Quick Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ridwaanhall/ngl-link-spamming.git
   cd ngl-link-spamming
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional):**

   ```bash
   cp config/.env.example .env
   # Edit .env file as needed
   ```

### Development Setup

For development with testing capabilities:

```bash
pip install -e .
pip install pytest pytest-cov
```

## 🎯 Usage

### Basic Usage

#### Custom Message Mode

```bash
python scripts/custom.py
```

#### Random Message Mode

```bash
python scripts/random.py
```

### Advanced Usage

#### Programmatic Usage

```python
from src.ngl_spammer.core.request_sender import RequestSender
from src.ngl_spammer.generators.device_generator import DeviceIDGenerator
from src.ngl_spammer.generators.message_generator import MessageGenerator

# Initialize components
sender = RequestSender()
device_gen = DeviceIDGenerator()
message_gen = MessageGenerator()

# Send a single message
device_id = device_gen.generate()
message = message_gen.generate()

response = sender.send_request_with_retry(
    username="target_user",
    question=message,
    device_id=device_id
)
```

#### Bulk Operations

```python
# Send multiple messages with adaptive delays
requests_data = [
    {
        "question": "Hello!",
        "device_id": device_gen.generate(),
        "game_slug": "confessions"
    }
    # ... more requests
]

responses = sender.send_bulk_requests("target_user", requests_data)
```

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:

```env
# API Configuration
NGL_API_URL=https://ngl.link/api/submit

# Request Configuration
DEFAULT_TIMEOUT=10
MAX_RETRIES=3
DEFAULT_DELAY=3.0
MIN_DELAY=1.0
MAX_DELAY=15.0

# Spam Configuration
DEFAULT_SPAM_COUNT=9999

# Logging Configuration
LOG_LEVEL=INFO
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/ngl_spammer

# Run specific test file
pytest tests/test_device_generator.py
```

## 📚 Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [Configuration Guide](config/.env.example) - Environment configuration options

## 🔧 Advanced Features

### Rate Limiting Protection

- Automatic delay adjustment based on response patterns
- Randomized request timing to avoid detection
- Intelligent retry mechanisms for failed requests

### IP Rotation

- Realistic IP address generation
- Header spoofing with random User-Agent strings
- Geographic region simulation

### Monitoring & Logging

- Real-time progress tracking
- Success/failure statistics
- Configurable logging levels
- Request/response monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational purposes only. Please use responsibly and in accordance with NGL.link's terms of service. The developers are not responsible for any misuse of this software.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

### ridwaanhall

- Instagram: [@ridwaanhall](https://instagram.com/ridwaanhall)
- GitHub: [@ridwaanhall](https://github.com/ridwaanhall)

---

⭐ If you find this project useful, please consider giving it a star on GitHub!
