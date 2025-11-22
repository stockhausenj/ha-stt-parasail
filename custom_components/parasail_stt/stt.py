"""Support for Parasail speech-to-text service."""
from __future__ import annotations

from collections.abc import AsyncIterable
import io
import logging
from typing import Any

from openai import OpenAI

from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
    SpeechToTextEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_API_KEY,
    CONF_MODEL,
    DEFAULT_MODEL,
    DOMAIN,
    PARASAIL_API_BASE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Parasail STT platform."""
    async_add_entities([ParasailSTTEntity(config_entry)])


class ParasailSTTEntity(SpeechToTextEntity):
    """Parasail speech-to-text entity."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Parasail STT entity."""
        self._config_entry = config_entry
        self._attr_name = f"Parasail STT {config_entry.data.get(CONF_MODEL, DEFAULT_MODEL)}"
        self._attr_unique_id = config_entry.entry_id

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        # Whisper supports many languages
        return [
            "en",  # English
            "zh",  # Chinese
            "de",  # German
            "es",  # Spanish
            "ru",  # Russian
            "ko",  # Korean
            "fr",  # French
            "ja",  # Japanese
            "pt",  # Portuguese
            "tr",  # Turkish
            "pl",  # Polish
            "ca",  # Catalan
            "nl",  # Dutch
            "ar",  # Arabic
            "sv",  # Swedish
            "it",  # Italian
            "id",  # Indonesian
            "hi",  # Hindi
            "fi",  # Finnish
            "vi",  # Vietnamese
            "he",  # Hebrew
            "uk",  # Ukrainian
            "el",  # Greek
            "ms",  # Malay
            "cs",  # Czech
            "ro",  # Romanian
            "da",  # Danish
            "hu",  # Hungarian
            "ta",  # Tamil
            "no",  # Norwegian
            "th",  # Thai
            "ur",  # Urdu
            "hr",  # Croatian
            "bg",  # Bulgarian
            "lt",  # Lithuanian
            "la",  # Latin
            "mi",  # Maori
            "ml",  # Malayalam
            "cy",  # Welsh
            "sk",  # Slovak
            "te",  # Telugu
            "fa",  # Persian
            "lv",  # Latvian
            "bn",  # Bengali
            "sr",  # Serbian
            "az",  # Azerbaijani
            "sl",  # Slovenian
            "kn",  # Kannada
            "et",  # Estonian
            "mk",  # Macedonian
            "br",  # Breton
            "eu",  # Basque
            "is",  # Icelandic
            "hy",  # Armenian
            "ne",  # Nepali
            "mn",  # Mongolian
            "bs",  # Bosnian
            "kk",  # Kazakh
            "sq",  # Albanian
            "sw",  # Swahili
            "gl",  # Galician
            "mr",  # Marathi
            "pa",  # Punjabi
            "si",  # Sinhala
            "km",  # Khmer
            "sn",  # Shona
            "yo",  # Yoruba
            "so",  # Somali
            "af",  # Afrikaans
            "oc",  # Occitan
            "ka",  # Georgian
            "be",  # Belarusian
            "tg",  # Tajik
            "sd",  # Sindhi
            "gu",  # Gujarati
            "am",  # Amharic
            "yi",  # Yiddish
            "lo",  # Lao
            "uz",  # Uzbek
            "fo",  # Faroese
            "ht",  # Haitian Creole
            "ps",  # Pashto
            "tk",  # Turkmen
            "nn",  # Nynorsk
            "mt",  # Maltese
            "sa",  # Sanskrit
            "lb",  # Luxembourgish
            "my",  # Myanmar
            "bo",  # Tibetan
            "tl",  # Tagalog
            "mg",  # Malagasy
            "as",  # Assamese
            "tt",  # Tatar
            "haw", # Hawaiian
            "ln",  # Lingala
            "ha",  # Hausa
            "ba",  # Bashkir
            "jw",  # Javanese
            "su",  # Sundanese
        ]

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return list of supported audio formats."""
        # Whisper supports many formats, but we'll use the most common ones
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return list of supported audio codecs."""
        # Whisper is flexible with codecs
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return list of supported audio bit rates."""
        # Whisper can handle various bit rates
        return [AudioBitRates.BITRATE_16, AudioBitRates.BITRATE_32]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return list of supported audio sample rates."""
        # Whisper can handle various sample rates
        # Only use valid AudioSampleRates constants that exist in Home Assistant
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_22000,
            AudioSampleRates.SAMPLERATE_44000,
            AudioSampleRates.SAMPLERATE_48000,
        ]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return list of supported audio channels."""
        # Whisper can handle both mono and stereo
        return [AudioChannels.CHANNEL_MONO, AudioChannels.CHANNEL_STEREO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        """Process an audio stream to STT service."""
        _LOGGER.debug("Processing audio stream with metadata: %s", metadata)

        # Get configuration
        config = self._config_entry.options or self._config_entry.data
        api_key = self._config_entry.data[CONF_API_KEY]
        model = config.get(CONF_MODEL, DEFAULT_MODEL)

        # Collect audio data from stream
        audio_data = b""
        async for chunk in stream:
            audio_data += chunk

        _LOGGER.debug("Collected %d bytes of audio data", len(audio_data))

        if not audio_data:
            return SpeechResult(
                text="",
                result=SpeechResultState.ERROR,
            )

        # Determine filename based on format
        if metadata.format == AudioFormats.WAV:
            filename = "audio.wav"
        elif metadata.format == AudioFormats.OGG:
            filename = "audio.ogg"
        else:
            filename = "audio.raw"

        # Prepare language parameter - only pass if it's a valid 2-letter code
        language = None
        if metadata.language and len(metadata.language) == 2:
            language = metadata.language
            _LOGGER.debug("Using language: %s", language)

        # Determine content type based on format
        if metadata.format == AudioFormats.WAV:
            content_type = "audio/wav"
        elif metadata.format == AudioFormats.OGG:
            content_type = "audio/ogg"
        else:
            content_type = "application/octet-stream"

        _LOGGER.debug(
            "Transcribing audio: format=%s, language=%s, model=%s, size=%d bytes, content_type=%s",
            metadata.format,
            language,
            model,
            len(audio_data),
            content_type
        )

        # Perform transcription
        def _transcribe():
            """Perform transcription in executor."""
            # Create audio file object inside executor for thread safety
            audio_file = io.BytesIO(audio_data)
            audio_file.name = filename
            audio_file.seek(0)

            # Debug: Log first few bytes to verify audio data
            _LOGGER.debug(
                "Audio file first 16 bytes: %s",
                audio_data[:16].hex() if len(audio_data) >= 16 else audio_data.hex()
            )

            client = OpenAI(
                base_url=PARASAIL_API_BASE,
                api_key=api_key,
            )

            # Build request parameters - pass file as tuple for proper multipart encoding
            # Format: (filename, file_object, content_type)
            params = {
                "model": model,
                "file": (filename, audio_file, content_type),
            }

            # Only add language if specified
            if language:
                params["language"] = language

            _LOGGER.debug("Sending transcription request with params: model=%s, language=%s, content_type=%s",
                         model, language, content_type)

            transcription = client.audio.transcriptions.create(**params)

            return transcription.text

        try:
            text = await self.hass.async_add_executor_job(_transcribe)
            _LOGGER.debug("Transcription result: %s", text)

            return SpeechResult(
                text=text,
                result=SpeechResultState.SUCCESS,
            )
        except Exception as err:
            # Log detailed error information
            _LOGGER.error(
                "Error during transcription: %s (format=%s, language=%s, model=%s, size=%d bytes)",
                err,
                metadata.format,
                language,
                model,
                len(audio_data),
                exc_info=True
            )
            return SpeechResult(
                text="",
                result=SpeechResultState.ERROR,
            )
