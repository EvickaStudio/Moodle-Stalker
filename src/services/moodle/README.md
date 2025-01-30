# Moodle Integration Modules

## Overview

This directory contains modules for integrating with Moodle, a popular learning management system. The primary focus is on interacting with Moodle's API to fetch information and notifications.

### Modules

- [Moodle API Wrapper](#moodle-api-wrapper)
- [Notification Handler](#notification-handler)
- [Error Handling](#error-handling)

## Moodle API Wrapper

The `MoodleAPI` class provides a Python wrapper for interacting with the Moodle API. It implements the Singleton pattern and handles authentication, session management, and API requests.

### Features

- User authentication with Moodle
- Session management with consistent headers
- Site information retrieval
- User information lookup
- Notification fetching
- Error handling and logging

### API Usage

```python
from src.services.moodle.api import MoodleAPI
from src.core.config import Config

# Initialize with configuration
config = Config("config.ini")
moodle_api = MoodleAPI(config.moodle.url)

# Login
moodle_api.login(config.moodle.username, config.moodle.password)

# Get site information
site_info = moodle_api.get_site_info()
print(site_info)
```

## Notification Handler

The `MoodleNotificationHandler` class manages the fetching and processing of Moodle notifications. It provides:

- Automatic notification polling
- Type-safe notification processing
- User information caching
- Error handling with retries
- Rate limiting and backoff strategies

### Notification Handler Usage

```python
from src.services.moodle.notification_handler import MoodleNotificationHandler
from src.core.config import Config

config = Config("config.ini")
handler = MoodleNotificationHandler(config)

# Fetch new notifications
notification = handler.fetch_newest_notification()
if notification:
    print(f"New notification: {notification['subject']}")
```

## Error Handling

The module includes custom exceptions for better error handling:

- `MoodleError`: Base exception for all Moodle-related errors
- `MoodleConnectionError`: Raised when connection to Moodle fails
- `MoodleAuthenticationError`: Raised when authentication fails

### Example

```python
from src.services.moodle.errors import MoodleConnectionError, MoodleAuthenticationError

try:
    handler = MoodleNotificationHandler(config)
except MoodleAuthenticationError as e:
    print(f"Authentication failed: {e}")
except MoodleConnectionError as e:
    print(f"Connection error: {e}")
```

## Configuration

The Moodle integration requires the following configuration in your `config.ini`:

```ini
[moodle]
url = https://your.moodle.instance
username = your_username
password = your_password
```

## Extending the Integration

To extend the Moodle integration:

1. Add new methods to the `MoodleAPI` class for additional API endpoints
2. Implement new handlers for specific functionality
3. Add appropriate error handling and logging
4. Update type definitions as needed
5. Add tests for new functionality

For more details on the implementation, see the source code:

- [api.py](api.py) - API wrapper implementation
- [notification_handler.py](notification_handler.py) - Notification handling
- [errors.py](errors.py) - Custom exceptions
