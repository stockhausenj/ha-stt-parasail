"""Config flow for Parasail STT integration."""
from __future__ import annotations

import io
import logging
from typing import Any

from openai import OpenAI
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_API_KEY,
    CONF_MODEL,
    DEFAULT_MODEL,
    DOMAIN,
    PARASAIL_API_BASE,
    PARASAIL_STT_MODELS,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    def _test_connection():
        """Test connection to Parasail API."""
        client = OpenAI(
            base_url=PARASAIL_API_BASE,
            api_key=data[CONF_API_KEY],
        )
        # Create a minimal test audio file (silence)
        # Simple WAV file: 0.1 second of silence at 16kHz mono, 16-bit PCM
        import struct
        import wave

        # Create a minimal WAV file in memory
        audio_buffer = io.BytesIO()

        with wave.open(audio_buffer, 'wb') as wav_file:
            # Set WAV file parameters
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit = 2 bytes
            wav_file.setframerate(16000)  # 16kHz

            # Write 0.1 seconds of silence (1600 samples)
            num_samples = 1600
            silence = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))
            wav_file.writeframes(silence)

        # Reset buffer position to beginning
        audio_buffer.seek(0)
        audio_buffer.name = "test.wav"

        return client.audio.transcriptions.create(
            model=data.get(CONF_MODEL, DEFAULT_MODEL),
            file=audio_buffer,
        )

    try:
        # Test the API key with a simple transcription
        await hass.async_add_executor_job(_test_connection)
    except Exception as err:
        _LOGGER.error("Failed to connect to Parasail API: %s", err)
        raise InvalidAuth from err

    return {"title": f"Parasail STT ({data.get(CONF_MODEL, DEFAULT_MODEL)})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Parasail STT."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_MODEL, default=DEFAULT_MODEL): vol.In(
                        PARASAIL_STT_MODELS
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Parasail STT."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        super().__init__()

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current options, fallback to data if options not set
        config_entry = self.config_entry
        options = config_entry.options or config_entry.data

        schema_dict = {
            vol.Required(
                CONF_MODEL,
                default=options.get(CONF_MODEL, DEFAULT_MODEL),
            ): vol.In(PARASAIL_STT_MODELS),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
        )


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
