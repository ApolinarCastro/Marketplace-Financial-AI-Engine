import datetime

class Observer:
    @staticmethod
    def trace(action_type, name, status="STARTED", details=""):
        log_entry = f"[{datetime.datetime.now().isoformat()}] [{action_type}] {name} - {status} - {details}"
        print(log_entry)
        with open("aesp_execution.log", "a") as f:
            f.write(log_entry + "\n")
