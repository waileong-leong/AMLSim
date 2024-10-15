import random
from typing import Optional
import sys
import json

class ModelParameters:
    rand = random.Random()
    prop: Optional[dict] = None

    SAR2SAR_EDGE_THRESHOLD = 0.0
    SAR2NORMAL_EDGE_THRESHOLD = 0.0
    NORMAL2SAR_EDGE_THRESHOLD = 0.0
    NORMAL2NORMAL_EDGE_THRESHOLD = 0.0
    
    SAR2SAR_TX_PROB = 1.0
    SAR2NORMAL_TX_PROB = 1.0
    NORMAL2SAR_TX_PROB = 1.0
    NORMAL2NORMAL_TX_PROB = 1.0

    SAR2SAR_AMOUNT_RATIO = 1.0
    SAR2NORMAL_AMOUNT_RATIO = 1.0
    NORMAL2SAR_AMOUNT_RATIO = 1.0
    NORMAL2NORMAL_AMOUNT_RATIO = 1.0

    NORMAL_HIGH_RATIO = 1.0
    NORMAL_LOW_RATIO = 1.0
    NORMAL_HIGH_PROB = 0.0
    NORMAL_LOW_PROB = 0.0
    NORMAL_SKIP_PROB = 0.0

    @classmethod
    def is_valid(cls) -> bool:
        return cls.prop is not None

    @classmethod
    def get_ratio(cls, key: str, default_value: float = 1.0) -> float:
        return float(cls.prop.get(key, default_value))

    @classmethod
    def load_properties(cls, prop_file: Optional[str]):
        if prop_file is None:
            return
        print(f"Model parameter file: {prop_file}")
        try:
            with open(prop_file, 'r') as f:
                cls.prop = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in file: {prop_file}")
            print(e)
            cls.prop = None
            return
        except IOError as e:
            print(f"Cannot load model parameter file: {prop_file}")
            print(e)
            cls.prop = None
            return

        cls.SAR2SAR_EDGE_THRESHOLD = cls.get_ratio("sar2sar_edge_threshold")
        cls.SAR2NORMAL_EDGE_THRESHOLD = cls.get_ratio("sar2normal_edge_threshold")
        cls.NORMAL2SAR_EDGE_THRESHOLD = cls.get_ratio("normal2sar_edge_threshold")
        cls.NORMAL2NORMAL_EDGE_THRESHOLD = cls.get_ratio("normal2normal_edge_threshold")
        
        cls.SAR2SAR_TX_PROB = cls.get_ratio("sar2sar_tx_prob")
        cls.SAR2NORMAL_TX_PROB = cls.get_ratio("sar2normal_tx_prob")
        cls.NORMAL2SAR_TX_PROB = cls.get_ratio("normal2sar_tx_prob")
        cls.NORMAL2NORMAL_TX_PROB = cls.get_ratio("normal2normal_tx_prob")

        cls.SAR2SAR_AMOUNT_RATIO = cls.get_ratio("sar2sar_amount_ratio")
        cls.SAR2NORMAL_AMOUNT_RATIO = cls.get_ratio("sar2normal_amount_ratio")
        cls.NORMAL2SAR_AMOUNT_RATIO = cls.get_ratio("normal2sar_amount_ratio")
        cls.NORMAL2NORMAL_AMOUNT_RATIO = cls.get_ratio("normal2normal_amount_ratio")

        cls.NORMAL_HIGH_RATIO = cls.get_ratio("normal_high_ratio", 1.0)
        cls.NORMAL_LOW_RATIO = cls.get_ratio("normal_low_ratio", 1.0)
        cls.NORMAL_HIGH_PROB = cls.get_ratio("normal_high_prob", 0.0)
        cls.NORMAL_LOW_PROB = cls.get_ratio("normal_low_prob", 0.0)
        cls.NORMAL_SKIP_PROB = cls.get_ratio("normal_skip_prob", 0.0)

        if cls.NORMAL_HIGH_RATIO < 1.0:
            raise ValueError("The high transaction amount ratio must be 1.0 or more")
        if cls.NORMAL_LOW_RATIO <= 0.0 or 1.0 < cls.NORMAL_LOW_RATIO:
            raise ValueError("The low transaction amount ratio must be positive and 1.0 or less")
        if 1.0 < cls.NORMAL_HIGH_PROB + cls.NORMAL_LOW_PROB + cls.NORMAL_SKIP_PROB:
            raise ValueError("The sum of high, low and skip transaction probabilities must be 1.0 or less")

        print("Transaction Probability:")
        print(f"\tSAR -> SAR: {cls.SAR2SAR_TX_PROB}")
        print(f"\tSAR -> Normal: {cls.SAR2NORMAL_TX_PROB}")
        print(f"\tNormal -> SAR: {cls.NORMAL2SAR_TX_PROB}")
        print(f"\tNormal -> Normal: {cls.NORMAL2NORMAL_TX_PROB}")

        print("Transaction edge addition threshold (proportion of SAR accounts):")
        print(f"\tSAR -> SAR: {cls.SAR2SAR_EDGE_THRESHOLD}")
        print(f"\tSAR -> Normal: {cls.SAR2NORMAL_EDGE_THRESHOLD}")
        print(f"\tNormal -> SAR: {cls.NORMAL2SAR_EDGE_THRESHOLD}")
        print(f"\tNormal -> Normal: {cls.NORMAL2NORMAL_EDGE_THRESHOLD}")

        print("Transaction amount ratio:")
        print(f"\tSAR -> SAR: {cls.SAR2SAR_AMOUNT_RATIO}")
        print(f"\tSAR -> Normal: {cls.SAR2NORMAL_AMOUNT_RATIO}")
        print(f"\tNormal -> SAR: {cls.NORMAL2SAR_AMOUNT_RATIO}")
        print(f"\tNormal -> Normal: {cls.NORMAL2NORMAL_AMOUNT_RATIO}")

    @classmethod
    def generate_amount_ratio(cls) -> float:
        return cls.rand.uniform(0.9, 1.1)

    @classmethod
    def adjust_amount(cls, orig: 'Account', bene: 'Account', base_amount: float) -> float:
        amount = base_amount * cls.generate_amount_ratio()

        if not cls.is_valid():
            return amount

        ratio = 1.0
        prob = cls.rand.random()
        
        if orig.is_sar():
            if bene.is_sar():
                if cls.SAR2SAR_TX_PROB <= prob:
                    return 0.0
                ratio = cls.SAR2SAR_AMOUNT_RATIO
            else:
                if cls.SAR2NORMAL_TX_PROB <= prob:
                    return 0.0
                ratio = cls.SAR2NORMAL_AMOUNT_RATIO
        else:
            if bene.is_sar():
                if cls.NORMAL2SAR_TX_PROB <= prob:
                    return 0.0
                ratio = cls.NORMAL2SAR_AMOUNT_RATIO
            else:
                if cls.NORMAL2NORMAL_TX_PROB <= prob:
                    return 0.0
                ratio = cls.NORMAL2NORMAL_AMOUNT_RATIO
            
            prob = cls.rand.random()
            if prob < cls.NORMAL_HIGH_PROB:
                ratio *= cls.NORMAL_HIGH_RATIO
            elif prob < cls.NORMAL_HIGH_PROB + cls.NORMAL_LOW_PROB:
                ratio *= cls.NORMAL_LOW_RATIO
            elif prob < cls.NORMAL_HIGH_PROB + cls.NORMAL_LOW_PROB + cls.NORMAL_SKIP_PROB:
                return 0.0

        return amount * ratio

    @classmethod
    def should_add_edge(cls, orig: 'Account', bene: 'Account') -> bool:
        if not cls.is_valid():
            return True

        num_neighbors = len(orig.get_bene_list())
        prop_sar_bene = orig.get_prop_sar_bene()

        if orig.is_sar():
            if bene.is_sar():
                return prop_sar_bene >= cls.SAR2SAR_EDGE_THRESHOLD
            else:
                return prop_sar_bene >= cls.SAR2NORMAL_EDGE_THRESHOLD
        else:
            if bene.is_sar():
                if cls.NORMAL2SAR_EDGE_THRESHOLD <= 0.0:
                    return True
                return num_neighbors > int(1 / cls.NORMAL2SAR_EDGE_THRESHOLD) and prop_sar_bene >= cls.NORMAL2SAR_EDGE_THRESHOLD
            else:
                return prop_sar_bene >= cls.NORMAL2NORMAL_EDGE_THRESHOLD