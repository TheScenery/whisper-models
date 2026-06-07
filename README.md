# Whisper Models

通过 GitHub Actions 自动下载 OpenAI Whisper 模型文件并上传到 Hugging Face Hub，解决 `whisper` 命令行运行时因网络原因下载模型失败的问题。

模型托管于：[https://huggingface.co/TheScenery/whisper-models](https://huggingface.co/TheScenery/whisper-models)

## 使用方法

### 安装依赖

```bash
pip install -U huggingface_hub
```

### 下载模型

```bash
# 下载单个模型到 whisper 缓存目录
huggingface-cli download TheScenery/whisper-models tiny.pt \
  --local-dir ~/.cache/whisper/

# 批量下载所有小模型
for model in tiny.en tiny base.en base small.en small medium.en medium; do
  huggingface-cli download TheScenery/whisper-models ${model}.pt \
    --local-dir ~/.cache/whisper/
done

# 批量下载大模型（无 2GB 限制）
for model in large-v1 large-v2 large-v3 large-v3-turbo; do
  huggingface-cli download TheScenery/whisper-models ${model}.pt \
    --local-dir ~/.cache/whisper/
done
```

### 国内用户（镜像加速）

```bash
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
  TheScenery/whisper-models tiny.pt --local-dir ~/.cache/whisper/
```

### 使用 whisper

模型文件放入 `~/.cache/whisper/` 后，whisper 会自动使用本地缓存:

```bash
whisper audio.mp3 --model tiny
```

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

## 配置

### GitHub Secrets

| Secret | 说明 |
|--------|------|
| `HF_TOKEN` | Hugging Face 访问令牌，需有写入权限 |

在 Actions 中手动触发 **Upload Whisper Models to Hugging Face** 即可自动下载并上传。

> 旧方案（GitHub Releases + split）已废弃，详见 git history。
