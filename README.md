# Parasail Speech-to-Text for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that provides speech-to-text (STT) capabilities using Parasail AI's Whisper models.

## Features

- **High-Quality Speech Recognition**: Uses OpenAI's Whisper models hosted on Parasail AI
- **Multiple Language Support**: Supports 90+ languages
- **Easy Configuration**: Simple setup through Home Assistant UI
- **Model Selection**: Choose between Whisper Large v3 and Whisper Large v3 Turbo
- **Privacy-Focused**: Uses Parasail AI's secure API

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/stockhausenj/ha-stt-parasail`
5. Select "Integration" as the category
6. Click "Add"
7. Find "Parasail Speech-to-Text" in the integration list and click "Download"
8. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/parasail_stt` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Parasail Speech-to-Text"
4. Enter your Parasail API key (get one at https://www.parasail.io/)
5. Select your preferred Whisper model
6. Click "Submit"

## Usage

Once configured, the Parasail STT provider will be available in Home Assistant. You can use it with:

- **Assist Pipeline**: Configure it as your STT provider in Settings → Voice Assistants
- **Wyoming Protocol**: Use it with voice satellites and other STT consumers
- **Automations**: Use the STT service in your automation scripts

### Example: Configure in Assist Pipeline

1. Go to Settings → Voice Assistants
2. Create a new assistant or edit an existing one
3. Under "Speech-to-text", select "Parasail STT"
4. Save your changes

## Supported Models

- `openai/whisper-large-v3-turbo` (Default, Recommended)
  - Faster processing
  - Lower latency
  - Excellent accuracy

- `openai/whisper-large-v3`
  - Slightly better accuracy
  - Higher latency
  - More resource-intensive

## Supported Languages

Whisper supports 90+ languages including:
English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, and many more.

## API Key

You need a Parasail API key to use this integration. Get one at:
https://www.parasail.io/

Parasail offers competitive pricing for API access to Whisper models.

## Troubleshooting

### "Invalid API key" error
- Verify your API key is correct
- Check that your Parasail account is active
- Ensure you have sufficient API credits

### STT not working in Assist
- Make sure the integration is properly configured
- Check Home Assistant logs for errors
- Verify your audio input device is working

### Poor transcription quality
- Try switching to the `whisper-large-v3` model
- Ensure clear audio input
- Check microphone placement and quality

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/stockhausenj/ha-stt-parasail/issues).

## License

This project is licensed under the MIT License.

## Credits

- Built using [Parasail AI](https://www.parasail.io/)
- Powered by OpenAI's Whisper models
- Inspired by the Home Assistant community
