# Whisper Models

自动下载 OpenAI Whisper 模型文件并通过 GitHub Releases 分发，解决 `whisper` 命令行运行时因网络原因下载模型失败的问题。

## 下载模型

从 [Releases](https://github.com/你的用户名/whisper-models/releases/tag/latest) 页面下载所需的 `.pt` 文件，
放入 Whisper 缓存目录:

### 小模型（< 2GB）

可直接下载:

```bash
# macOS / Linux
curl -L -o ~/.cache/whisper/tiny.pt \
  https://github.com/你的用户名/whisper-models/releases/download/latest/tiny.pt

# 批量下载小模型
for model in tiny.en tiny base.en base small.en small medium.en medium; do
  curl -L -o ~/.cache/whisper/${model}.pt \
    https://github.com/你的用户名/whisper-models/releases/download/latest/${model}.pt
done
```

### 大模型（>= 2GB）

因 GitHub Releases 单文件限制 2GB，large 系列模型已分割上传，使用 `scripts/join.sh` 自动下载、重组并校验:

```bash
bash scripts/join.sh large-v3
```

## 使用

模型文件放入 `~/.cache/whisper/` 后，whisper 会自动使用本地缓存，无需再从 OpenAI 下载:

```bash
whisper audio.mp3 --model tiny
```

## 手动触发更新

在 GitHub 仓库页面点击 **Actions** → **Download Whisper Models** → **Run workflow** 即可重新下载最新模型。

## 可用模型

| 模型 | 大小 | 多语言 |
|------|------|--------|
| tiny.en | ~75 MB | 仅英文 |
| tiny | ~75 MB | 多语言 |
| base.en | ~142 MB | 仅英文 |
| base | ~142 MB | 多语言 |
| small.en | ~466 MB | 仅英文 |
| small | ~466 MB | 多语言 |
| medium.en | ~1.5 GB | 仅英文 |
| medium | ~1.5 GB | 多语言 |
| large-v1 | ~2.9 GB | 多语言 |
| large-v2 | ~2.9 GB | 多语言 |
| large-v3 | ~2.9 GB | 多语言 |
| large-v3-turbo | ~2.9 GB | 多语言 |
