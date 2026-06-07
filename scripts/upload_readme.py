import os
from huggingface_hub import HfApi

token = os.environ["HF_TOKEN"]
repo_id = os.environ["HF_REPO_ID"]

api = HfApi(token=token)
api.upload_file(
    path_or_fileobj="HF_README.md",
    path_in_repo="README.md",
    repo_id=repo_id,
    token=token,
)
print("Model card uploaded")
