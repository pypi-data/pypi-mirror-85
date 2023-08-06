import subprocess
import json
import time
from io import StringIO

import typer

from savvihub import Context
from savvihub.common.constants import DEBUG

agent_app = typer.Typer()


@agent_app.callback(hidden=True)
def main():
    return


@agent_app.command()
def collect_system_metrics(
    metrics_collector_binary: str = typer.Option("system-metrics-collector", "--collector-binary"),
    prometheus_url: str = typer.Option(..., "--prometheus-url"),
    collect_period: int = typer.Option(5, "--collect-period", min=5),
):
    context = Context(experiment_required=True)
    client = context.authorized_client

    while True:
        time.sleep(collect_period)

        stderr = StringIO()
        output = subprocess.check_output([
            metrics_collector_binary,
            "-prometheus-url",
            prometheus_url,
            "-experiment",
            context.experiment.slug,
        ], stderr=stderr).decode('utf-8').strip()

        if not output:
            continue

        metrics = {}
        rows = json.loads(output)
        if not rows:
            continue

        for row in rows:
            metrics[row['name']] = [{
                'timestamp': float(row['timestamp']),
                'value': row['value'],
            }]

        if DEBUG:
            print(stderr.getvalue())

        client.experiment_system_metrics_update(context.experiment.id, metrics)
