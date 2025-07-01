# Squid Proxy with Docker

This project sets up a Squid proxy server using Docker, along with a mock ICAP server for request and response modification (`reqmod` and `respmod`).

## Usage

1. **Start the proxy and all services:**

   ```sh
   ./start.sh
   ```

   This script will automatically rebuild the Python-based services (`icap-server` and `mock-http-server`) before launching the environment with `docker-compose`.

2. The proxy will be available at `localhost:3128`.

## Configuration

- The Squid configuration is in `squid.conf`. It is pre-configured to use the mock ICAP server for `reqmod` and `respmod`.
- The mock ICAP server is written in Python and is located in the `icap` directory. It logs requests and responses but does not modify them.

## Stopping the services

```sh
docker-compose down
```
