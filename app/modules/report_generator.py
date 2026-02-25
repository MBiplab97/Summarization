import csv
import uuid

class ReportGenerator:

    async def generate_csv(self, results):
        filename = f"summary_{uuid.uuid4()}.csv"

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["file_name", "summary"])
            writer.writeheader()
            writer.writerows(results)

        return filename