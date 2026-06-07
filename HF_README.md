---
license: mit
library_name: whisper
pipeline_tag: automatic-speech-recognition
---

# Whisper Models

Pre-downloaded OpenAI Whisper model files, auto-updated via GitHub Actions.

## Usage

```bash
pip install -U huggingface_hub

huggingface-cli download TheScenery/whisper-models tiny.pt --local-dir ~/.cache/whisper/
```

Then use with whisper:

```bash
whisper audio.mp3 --model tiny
```

## Available Models

| Model | Size | Languages |
|-------|------|-----------|
| tiny.en | ~75 MB | English only |
| tiny | ~75 MB | Multilingual |
| base.en | ~142 MB | English only |
| base | ~142 MB | Multilingual |
| small.en | ~466 MB | English only |
| small | ~466 MB | Multilingual |
| medium.en | ~1.5 GB | English only |
| medium | ~1.5 GB | Multilingual |
| large-v1 | ~2.9 GB | Multilingual |
| large-v2 | ~2.9 GB | Multilingual |
| large-v3 | ~2.9 GB | Multilingual |
| large-v3-turbo | ~2.9 GB | Multilingual |

## Mirror for Chinese Users

```bash
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
  TheScenery/whisper-models tiny.pt --local-dir ~/.cache/whisper/
```
