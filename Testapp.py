from prometheus_client import start_http_server, Gauge
import time

container_state = Gauge("container_state", "State of the container", ["container_name"])
container_uptime_seconds = Gauge("container_uptime_seconds", "Uptimer of the container in seconds", ["container_name"])

def update_metrics(container_name, state, uptime_seconds):

    # Update the gauges with the provided values.
    container_state.labels(container_name=container_name).set(1 if state == 'running' else 0)
    container_uptime_seconds.labels(container_name=container_name).set(uptime_seconds)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Update metrics every second
    while True:
        # Replace the following lines with code to get real data
        container_info = [("grafana", "running", 1200), ("prometheus", "exited", 3600)]
        for info in container_info:
            update_metrics(*info)
        print("Server is running.")
        time.sleep(1)
