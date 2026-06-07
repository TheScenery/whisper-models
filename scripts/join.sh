#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-}"
RELEASE_URL="${2:-https://github.com/TheScenery/whisper-models/releases/download/latest}"

if [ -z "$MODEL" ]; then
  echo "Usage: $0 <model-name> [release-url]"
  echo ""
  echo "Download and join split model files into a single .pt file."
  echo ""
  echo "Examples:"
  echo "  $0 large-v3"
  echo "  $0 large-v2 https://mirror.example.com/whisper-models"
  echo ""
  echo "Available models: tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large-v3-turbo"
  exit 1
fi

CACHE_DIR="${HOME}/.cache/whisper"
mkdir -p "$CACHE_DIR"

echo "Downloading ${MODEL} parts from ${RELEASE_URL} ..."
# Download all parts
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Download SHA256 first to know what to expect
curl -fL -o "${TMPDIR}/${MODEL}.pt.sha256" "${RELEASE_URL}/${MODEL}.pt.sha256" 2>/dev/null || true

# Download all part files
for part_url in $(curl -sL "${RELEASE_URL}" | grep -oE "${MODEL}\.pt\.part-[a-z][a-z]" | sort -u); do
  echo "  Downloading ${part_url} ..."
  curl -fL -o "${TMPDIR}/${part_url}" "${RELEASE_URL}/${part_url}"
done

# If no parts found, try downloading the whole file directly
if [ -z "$(ls "${TMPDIR}/${MODEL}.pt.part-"* 2>/dev/null)" ]; then
  echo "  No split parts found, downloading full file..."
  curl -fL -o "${CACHE_DIR}/${MODEL}.pt" "${RELEASE_URL}/${MODEL}.pt"
  echo "Saved to ${CACHE_DIR}/${MODEL}.pt"
  exit 0
fi

echo "Joining parts..."
cat "${TMPDIR}/${MODEL}.pt.part-"* > "${TMPDIR}/${MODEL}.pt"

# Verify checksum
if [ -f "${TMPDIR}/${MODEL}.pt.sha256" ]; then
  EXPECTED=$(cut -d' ' -f1 "${TMPDIR}/${MODEL}.pt.sha256")
  ACTUAL=$(sha256sum "${TMPDIR}/${MODEL}.pt" | cut -d' ' -f1)
  if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "ERROR: SHA256 mismatch!"
    echo "  Expected: $EXPECTED"
    echo "  Actual:   $ACTUAL"
    exit 1
  fi
  echo "SHA256 verified: $ACTUAL"
fi

mv "${TMPDIR}/${MODEL}.pt" "${CACHE_DIR}/${MODEL}.pt"
echo "Saved to ${CACHE_DIR}/${MODEL}.pt"
