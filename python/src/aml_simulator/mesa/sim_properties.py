import os
import json
from typing import Dict, Any

class SimProperties:
    def __init__(self, json_name: str):
        with open(json_name, 'r') as file:
            json_data = json.load(file)

        default_prop = json_data["default"]
        self.general_prop = json_data["general"]
        self.sim_prop = json_data["simulator"]
        self.input_prop = json_data["temporal"]  # Input directory of this simulator is temporal directory
        self.output_prop = json_data["output"]

        self.normal_tx_interval = self.sim_prop["transaction_interval"]
        self.min_tx_amount = default_prop["min_amount"]
        self.max_tx_amount = default_prop["max_amount"]

        print(f"General transaction interval: {self.normal_tx_interval}")
        print(f"Base transaction amount: Normal = {self.min_tx_amount}, Suspicious = {self.max_tx_amount}")

        self.cash_in_prop = default_prop["cash_in"]
        self.cash_out_prop = default_prop["cash_out"]
        self.margin_ratio = default_prop["margin_ratio"]

        self.seed = int(os.environ.get("RANDOM_SEED", self.general_prop["random_seed"]))
        print(f"Random seed: {self.seed}")

        self.sim_name = os.environ.get("simulation_name") or self.general_prop["simulation_name"]
        print(f"Simulation name: {self.sim_name}")

        self.work_dir = os.path.join(self.input_prop["directory"], self.sim_name)
        print(f"Working directory: {self.work_dir}")

    @property
    def steps(self) -> int:
        return self.general_prop["total_steps"]

    @property
    def compute_diameter(self) -> bool:
        return self.sim_prop["compute_diameter"]

    @property
    def transaction_limit(self) -> int:
        return self.sim_prop["transaction_limit"]

    @property
    def num_branches(self) -> int:
        return self.sim_prop["numBranches"]

    def get_input_acct_file(self) -> str:
        return os.path.join(self.work_dir, self.input_prop["accounts"])

    def get_input_tx_file(self) -> str:
        return os.path.join(self.work_dir, self.input_prop["transactions"])

    def get_input_alert_member_file(self) -> str:
        return os.path.join(self.work_dir, self.input_prop["alert_members"])

    def get_normal_models_file(self) -> str:
        return os.path.join(self.work_dir, self.input_prop["normal_models"])

    def get_output_tx_log_file(self) -> str:
        return os.path.join(self.get_output_dir(), self.output_prop["transaction_log"])

    def get_output_dir(self) -> str:
        return os.path.join(self.output_prop["directory"], self.sim_name)

    def get_counter_log_file(self) -> str:
        return os.path.join(self.get_output_dir(), self.output_prop["counter_log"])

    def get_diameter_log_file(self) -> str:
        return os.path.join(self.work_dir, self.output_prop["diameter_log"])

    def get_cash_tx_interval(self, is_cash_in: bool, is_sar: bool) -> int:
        key = "fraud_interval" if is_sar else "normal_interval"
        return self.cash_in_prop[key] if is_cash_in else self.cash_out_prop[key]

    def get_cash_tx_min_amount(self, is_cash_in: bool, is_sar: bool) -> float:
        key = "fraud_min_amount" if is_sar else "normal_min_amount"
        return self.cash_in_prop[key] if is_cash_in else self.cash_out_prop[key]

    def get_cash_tx_max_amount(self, is_cash_in: bool, is_sar: bool) -> float:
        key = "fraud_max_amount" if is_sar else "normal_max_amount"
        return self.cash_in_prop[key] if is_cash_in else self.cash_out_prop[key]