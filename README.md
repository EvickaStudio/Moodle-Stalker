# Moodle Mate

<div align="center">
  <img src="assets/logo.svg" alt="Moodle Mate Logo" width="160">
  <h1>Moodle Mate</h1>
  <p><strong>Your Smart Moodle Notification Assistant</strong></p>
</div>

<p align="center">
  <a href="https://github.com/EvickaStudio/Moodle-Mate/actions"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/EvickaStudio/Moodle-Mate/ci.yml?+label=Build%20Status"></a>
  <a href="https://github.com/EvickaStudio/Moodle-Mate/blob/main/LICENSE.md"><img alt="GitHub license" src="https://img.shields.io/github/license/EvickaStudio/Moodle-Mate"></a>
  <a href="https://github.com/EvickaStudio/Moodle-Mate/commits"><img alt="Commits" src="https://img.shields.io/github/commit-activity/m/EvickaStudio/Moodle-Mate?label=commits"></a>
  <a href="https://github.com/EvickaStudio/Moodle-Mate/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/EvickaStudio/Moodle-Mate"></a>
  <a href="https://github.com/EvickaStudio/Moodle-Mate/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/EvickaStudio/Moodle-Mate"></a>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/EvickaStudio/Moodle-Mate">
</p>

## What is Moodle Mate?

Moodle Mate is an Python application that fetches notifications from a Moodle instance (eg. a school or university) and delivers them to a notification platform (eg. Discord). This will allow you to stay up to date with all your courses and activities without having to manually check your E-Mail or Moodle.

Moodle Mate comes with an optional AI-powered summarization feature that will summarize the notifications for you and add it as an small TLDR to the notification. BYOK - Bring your own key, you can use any AI provider you want that supports the openai api structure, so if you have privacy concerns you can use an local hosted model (e.g. with [Ollama](https://ollama.ai/)).

## Key Features

- **Smart Notification Management**
  - Automatic notification fetching and processing
  - AI-powered content summarization (optional)
  - HTML to Markdown notification conversion for better readability
    - Uses a Python port of turndown for the conversion -> [turndown-python](https://github.com/EvickaStudio/turndown-python)
  - Configurable update intervals and other settings

- **Multi-Platform Support**
  - Discord (via webhooks)
  - Support for additional notification platforms (TODO)
  - Modular architecture for easy integration of new platforms

- **AI Integration**
  - Support for multiple AI providers
  - Configurable models and parameters
  - Optional summarization feature

## Requirements

- Python 3.10 or higher
- Internet connection
- Moodle instance with API access/ REST API enabled

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/EvickaStudio/Moodle-Mate.git
   cd Moodle-Mate
   ```

2. **Install Dependencies**

   You can optionally use a virtual environment to install the dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   # soure venv/bin/activate.fish for fish shell
   ```

   Then install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Application**

   The recommended way is to use the config generator:

   ```bash
   python main.py --gen-config
   ```

   Alternatively, you can manually edit the `config.example.ini` file:

   ```bash
   cp config.example.ini config.ini
   # Edit config.ini with your settings
   ```

   For more information on the configuration, see the [Configuration](src/core/config/README.md) documentation.

## Usage

Start the application:

```bash
python main.py
```

The application will:

1. Validate your configuration
2. Connect to your Moodle instance
3. Start monitoring for new notifications
4. Process and deliver notifications according to your settings

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Apache License 2.0 - See [LICENSE.md](LICENSE.md) for details.

## Author

Created with ❤️ by [EvickaStudio](https://github.com/EvickaStudio)
