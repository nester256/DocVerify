#!/usr/bin/env bash

echo "Start worker service"
exec uv run taskiq worker src.utils.broker:broker src.utils.generate_pdf --log-level=INFO --workers=1
