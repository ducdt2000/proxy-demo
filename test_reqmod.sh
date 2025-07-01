#!/bin/bash
# This script sends a request specifically to test the REQMOD functionality.

PROXY_URL="http://localhost:3128"
TARGET_URL="http://mock-http-server:8000"

# We add a custom header to the request. This allows us to trace it.
# 1. Watch the 'icap-server' logs for the "Received REQMOD request" message.
# 2. Watch the 'mock-http-server' logs to see this custom header arriving.
CUSTOM_HEADER="X-Test-Reqmod: true"

echo "=> Sending a request to test REQMOD..."
echo "   Proxy: $PROXY_URL"
echo "   Target: $TARGET_URL"
echo "   Custom Header: '$CUSTOM_HEADER'"
echo
echo "=> Watch the logs of the 'icap-server' and 'mock-http-server' containers."
echo

curl -v -x "$PROXY_URL" -H "$CUSTOM_HEADER" "$TARGET_URL" 