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
- The mock ICAP server is written in Python and is located in the `icap` directory. It now includes X-Next-Services header support for dynamic service routing.

## X-Next-Services Feature

This setup now supports dynamic service chaining using the X-Next-Services ICAP response header:

- **Health Checking**: Each ICAP server checks the health of other services before routing
- **Dynamic Routing**: Services can dynamically route requests to healthy services using the X-Next-Services header
- **Load Balancing**: Requests are automatically routed to available services based on health status

### 🔒 Security Considerations

**Important**: The X-Next-Services feature requires careful security consideration:

1. **Trust Model**: When `routing=on` is enabled, Squid trusts the ICAP service to make routing decisions
2. **Service Validation**: Squid only accepts service names that are configured in `squid.conf`
3. **Whitelist Protection**: The ICAP server includes a whitelist of allowed services per host
4. **Audit Logging**: All routing decisions are logged for security auditing

**Recommendation**: Only enable `routing=on` for trusted ICAP services in secure environments.

### Testing X-Next-Services

Run the test script to see the functionality in action:

```sh
python3 test_x_next_services.py
```

Then check the logs to see health checks and routing decisions:

```sh
docker-compose logs icap-server icap-server2
```

## Stopping the services

```sh
docker-compose down
```
