# Whisper Models

通过 GitHub Actions 自动下载 OpenAI Whisper 模型文件并上传到 Hugging Face Hub。

模型托管于：[huggingface.co/TheScenery/whisper-models](https://huggingface.co/TheScenery/whisper-models)

## 工作流程

1. 手动触发或每月定时运行 Actions
2. 并行下载所有 Whisper 模型（12 个）
3. 校验 SHA256
4. 上传到 Hugging Face Hub（已存在的文件自动跳过）

## 手动触发

**Actions** → **Upload Whisper Models to Hugging Face** → **Run workflow**

## 本地运行

```bash
pip install huggingface-hub
HF_TOKEN=hf_your_token python scripts/upload_model.py tiny
```

## 项目结构

```
.github/workflows/download-models.yml   # GitHub Actions 工作流
scripts/
  upload_model.py      # 下载 + 校验 + 上传单个模型
  upload_readme.py     # 上传 HF_README.md 到 HF 作为 model card
HF_README.md           # Hugging Face 仓库的 model card
README.md              # 本文件，GitHub 仓库说明
```
