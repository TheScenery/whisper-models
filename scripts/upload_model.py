import os
import sys
import hashlib
import urllib.request

from huggingface_hub import HfApi

MODEL_URLS = {
    "tiny.en":        ("d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03", "tiny.en.pt"),
    "tiny":           ("65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9", "tiny.pt"),
    "base.en":        ("25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead", "base.en.pt"),
    "base":           ("ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e", "base.pt"),
    "small.en":       ("f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872", "small.en.pt"),
    "small":          ("9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794", "small.pt"),
    "medium.en":      ("d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f", "medium.en.pt"),
    "medium":         ("345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1", "medium.pt"),
    "large-v1":       ("e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a", "large-v1.pt"),
    "large-v2":       ("81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524", "large-v2.pt"),
    "large-v3":       ("e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb", "large-v3.pt"),
    "large-v3-turbo": ("aff26ae408abcba5fbf8813c21e62b0941638c5f6eebfb145be0c9839262a19a", "large-v3-turbo.pt"),
}


def main():
    model_name = sys.argv[1]
    sha256, filename = MODEL_URLS[model_name]
    url = f"https://openaipublic.azureedge.net/main/whisper/models/{sha256}/{filename}"

    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO_ID", "TheScenery/whisper-models")

    if not token:
        print("ERROR: HF_TOKEN environment variable is required")
        sys.exit(1)

    print(f"[{model_name}] Downloading from OpenAI...")
    urllib.request.urlretrieve(url, filename)

    print(f"[{model_name}] Verifying SHA256...")
    with open(filename, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != sha256:
        print(f"SHA256 mismatch!\n  Expected: {sha256}\n  Actual:   {actual}")
        sys.exit(1)
    print(f"[{model_name}] SHA256 verified: {actual}")

    api = HfApi(token=token)

    print(f"[{model_name}] Uploading to Hugging Face Hub ({repo_id})...")
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id=repo_id,
        token=token,
    )

    print(f"[{model_name}] Done!")
    os.remove(filename)


if __name__ == "__main__":
    main()
