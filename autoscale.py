import time
from prometheus_api_client import PrometheusConnect
from google.cloud import compute_v1

prometheus_url = "http://192.168.139.128:9090"
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

cpu_query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'

def get_cpu_usage():
    result = prom.custom_query(query=cpu_query)
    cpu = float(result[0]['value'][1])
    return cpu

def create_gcp_vm():
    instance_client = compute_v1.InstancesClient()
    operation = instance_client.insert_unary(
        project="auto-scale-project-454613",
        zone="us-central1-a",
        instance_resource={
            "name": "autoscaled-vm",
            "machine_type": "zones/us-central1-a/machineTypes/e2-medium",
            "disks": [{
                "boot": True,
                "auto_delete": True,
                "initialize_params": {
                    "source_image": "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
                }
            }],
            "network_interfaces": [{
                "network": "global/networks/default",
                "access_configs": [{"name": "External NAT"}]
            }]
        }
    )
    print(f"GCP instance creation triggered: {operation.name}")

while True:
    cpu_usage = get_cpu_usage()
    print(f"CPU usage: {cpu_usage:.2f}%")
    if cpu_usage > 75:
        print("CPU threshold exceeded, scaling to GCP...")
        create_gcp_vm()
        break
    time.sleep(10)

