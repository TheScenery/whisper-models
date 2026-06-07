import ast
import os
import sys
import hashlib
import urllib.request

from huggingface_hub import HfApi

WHISPER_SOURCE = "https://raw.githubusercontent.com/openai/whisper/main/whisper/__init__.py"


def get_model_urls() -> dict:
    content = urllib.request.urlopen(WHISPER_SOURCE).read().decode("utf-8")
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "_MODELS" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise RuntimeError("_MODELS not found in whisper source")


def get_model_url(name: str) -> tuple[str, str, str]:
    models = get_model_urls()
    url = models[name]
    sha256 = url.split("/")[-2]
    filename = url.split("/")[-1]
    return url, sha256, filename


def main():
    model_name = sys.argv[1]
    token = os.environ.get("HF_TOKEN")
    repo_id = os.environ.get("HF_REPO_ID", "TheScenery/whisper-models")

    if not token:
        print("ERROR: HF_TOKEN environment variable is required")
        sys.exit(1)

    print(f"[{model_name}] Fetching model info from openai/whisper...")
    url, expected_sha256, filename = get_model_url(model_name)

    api = HfApi(token=token)

    if api.file_exists(repo_id=repo_id, filename=filename, repo_type="model"):
        print(f"[{model_name}] Already exists on HF Hub, skipping")
        return

    print(f"[{model_name}] Downloading from OpenAI...")
    urllib.request.urlretrieve(url, filename)

    print(f"[{model_name}] Verifying SHA256...")
    with open(filename, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != expected_sha256:
        print(f"SHA256 mismatch!\n  Expected: {expected_sha256}\n  Actual:   {actual}")
        sys.exit(1)
    print(f"[{model_name}] SHA256 verified: {actual}")

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
