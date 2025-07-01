#!/bin/bash
# A simple script to test the Squid proxy using curl.

PROXY_URL="http://localhost:3128"
TARGET_URL="http://mock-http-server:8000"

echo "Making a request to $TARGET_URL through proxy $PROXY_URL..."

curl -v -x "$PROXY_URL" "$TARGET_URL" 