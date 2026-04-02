#!/bin/bash
# Run this script to push Claude's changes to GitHub
cd "$(dirname "$0")"
git add -A
git commit -m "${1:-Claude: update repo}"
git push
echo "Done! Changes pushed to GitHub."
