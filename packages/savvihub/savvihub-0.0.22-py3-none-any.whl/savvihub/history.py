from datetime import datetime


class History:
    def __init__(self, experiment):
        self.experiment = experiment
        self.rows = []
        self._step_index = 0

    def update(self, client, step, row):
        """
        Update row in history
        """
        for k, v in row.items():
            if type(v) != str:
                row[k] = str(v)

        row["step"] = str(step)
        row["created_dt"] = datetime.utcnow().isoformat()
        self.request(client, row)
        self.rows.append(row)

    def request(self, client, row):
        _ = client.experiment_progress_update(self.experiment.id, row)
