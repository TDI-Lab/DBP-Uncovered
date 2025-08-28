import json
import copy
import os

# --- Base Template for all settings files ---
# All generated files will use this as a starting point.
BASE_SETTINGS_TEMPLATE = {
    "DBP-merged": True,
    "dec_matrix_settings": {
        "input_file": "./input/input_data_topsis_IQR_merge-DBP_all-DBP.xlsx",
        "cost_time_setting": "IQR",
        "collect_DBP": "all-DBP"
    },
    "DBP_ranking": {
        "THM": 1, "IDBP": 1, "BrDBP": 1, "HAA": 2, "HAN": 3, "CB": 4,
        "NS": 5, "HAL": 6, "HAM": 7, "HNM": 8, "HBQ": 9, "PDBP": 10,
        "HP": 11, "BPA": 12, "VOC": 12, "HDBP": 12, "AOX": 12
    },
    "action_category_ranking": {
        "RW": 1, "CA": 1, "PN": 1, "PC": 1, "FL": 1, "BL": 1,
        "CK": 1, "A_other": 1
    },
    "weight_settings": {
        "all_DBP": {"type": 1, "weight": 0},
        "cost_tier": {"type": 1, "weight": 0},
        "time_tier": {"type": 1, "weight": 0},
        "repeat_tier": {"type": 1, "weight": 0}
    }
}

def generate_settings_file(settings_name, weight_dict):
    """
    Creates a new .json settings file from the base template.

    Args:
        settings_name (str): The name for the settings scenario (e.g., "expert-weights").
        weight_dict (dict): A dictionary with the weights for the 4 main criteria.
    """
    # Create a deep copy to avoid modifying the original template
    new_settings = copy.deepcopy(BASE_SETTINGS_TEMPLATE)

    # Update the settings_name
    new_settings["settings_name"] = settings_name

    # Update the weights
    for key, weight_value in weight_dict.items():
        if key in new_settings["weight_settings"]:
            new_settings["weight_settings"][key]["weight"] = weight_value
        else:
            print(f"Warning: Key '{key}' not found in template's weight_settings.")

    # Define the output filename
    output_filename = os.path.join(os.path.dirname(__file__), f"{settings_name}_settings.json")

    # Write the dictionary to a JSON file
    with open(output_filename, 'w') as f:
        json.dump(new_settings, f, indent=4)
    
    print(f"Successfully generated: {output_filename}")


if __name__ == "__main__":
    # --- Scenario 1: Expert Weights ---
    expert_weights = {
        "all_DBP": 0.428,
        "cost_tier": 0.142,
        "time_tier": 0.215,
        "repeat_tier": 0.215
    }
    generate_settings_file("expert-weights", expert_weights)

    # --- Scenario 2: Conjoint Analysis Weights ---
    conjoint_weights = {
        "all_DBP": 0.286,
        "cost_tier": 0.303,
        "time_tier": 0.151,
        "repeat_tier": 0.26
    }
    generate_settings_file("conjoint_analysis", conjoint_weights)

    # --- Scenario 3: High DBP Focus (0.828) ---
    remaining_weight_1 = round((1 - 0.828) / 3, 4)
    high_dbp_weights = {
        "all_DBP": 0.828,
        "cost_tier": remaining_weight_1,
        "time_tier": remaining_weight_1,
        "repeat_tier": remaining_weight_1
    }
    generate_settings_file("high_dbp_focus", high_dbp_weights)

    # --- Scenarios 4-7: "What-if" analysis with one criterion at 0.85 ---
    criteria_keys = ["all_DBP", "cost_tier", "time_tier", "repeat_tier"]
    remaining_weight_2 = round((1 - 0.85) / 3, 4)

    for focus_key in criteria_keys:
        what_if_weights = {}
        for key in criteria_keys:
            if key == focus_key:
                what_if_weights[key] = 0.85
            else:
                what_if_weights[key] = remaining_weight_2
        
        # Generate a descriptive name for the file
        scenario_name = f"high_{focus_key}"
        generate_settings_file(scenario_name, what_if_weights)

    print("\nAll settings files have been generated in the input directory.")

