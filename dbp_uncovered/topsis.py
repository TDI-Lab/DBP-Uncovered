import os
import shutil
import logging
import sys
import argparse
import time
import json

# Add path so we can import acronym_dictionary
sys.path.append('../')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

# Data analysis
import pandas as pd
import numpy as np
from scipy.stats import rankdata # for ranking the candidates

# Own imports
from acronym_dictionary import direct_acronym_keyword_dict

'''
Script that performs the TOPSIS analysis using a settings files which is provided
through command-line arguments. 

I.e., 

python run_TOPSIS.py -s example_settings.json

It also preps and checks the data before.

Results are saved to ./output/ with additional directory structuring and naming
based on the information containing within the settings file.
'''

def check_data(input_df, map_acronyms = False):
    """Check the data before analysis, some DBP-related actions are completely
    empty (for example if only positive/negative measurements were made for a 
    certain DBP). This function adds a 1 to all entries in such cases for numerical
    reasons,

    Args:
        input_df (DataFrame): Dataframe containing the TOPSIS input data
        map_acronyms (bool, optional): Whether to map the action acronyms to their
        full meaning. Defaults to False.

    Returns:
        DataFrame: Dataframe containing the TOPSIS the altered data.
    """
    
    # Identify columns where all entries are 0
    cols_with_all_zeros = list(input_df.columns[(input_df == 0).all()])
    
    # Add 1 to these columns
    # This is because all zero columns give problems later when normalising the 
    # columns in the TOPSIS calculations. This is therefore purely for numerical
    # reasons but should have no effect on results given the normalising nature 
    # of different columns in a TOPSIS analysis
    
    if cols_with_all_zeros:
        input_df[cols_with_all_zeros] = input_df[cols_with_all_zeros] + 1
        logging.warning(f"The following columns were adjusted by adding 1 due to their values being all 0: {list(cols_with_all_zeros)} ")
    else:
        logging.info("No columns with all zero values found.")
    
    if map_acronyms:
        input_df.index = input_df.index.map(direct_acronym_keyword_dict)
    
    return input_df

def check_criteria(input_df, settings_dict, action_rank_dict):
    """Performs some checks on the criteria that will be used for the TOPSIS 
    analysis:
    1) Map the general action category to ranking defined in settings,
    2) Check if all columns in data have assigned values
    3) Generate a one-on-one dictionary that denotes the type of criteria for each
    of the criteria (i.e., higher values = good/bad)

    Args:
        input_df (DataFrame): Dataframe containing the TOPSIS input data
        settings_dict (Dict): Contains the TOPSIS settings
        action_rank_dict (Dict): Contains the rankings of different action 
        categories

    Returns:
        [Dataframe, Dict]: Dataframe with mapped action_tier, and Dict with 
        one-on-one key/value pairs of criteria/criteria_type
    """
    
    # Check if all columns in data have assigned values
    data_columns = list(input_df.keys())
    settings_keys = list(settings_dict.keys())
    
    # Ensure only criteria in the settings dictionary are kept
    special_keys = []
    for s_key in settings_keys:
        
        if s_key.startswith(("all", "positive", "negative", "other")):
            DBP_keys = [x for x in data_columns if x.startswith(s_key.split('_')[0]+'_')]
            special_keys.extend(DBP_keys)
        else:
            special_keys.append(s_key)
            
    input_df = input_df.drop(columns=[col for col in input_df if col not in special_keys])
    
    
    # Map general category types to ranking from settings if present
    if 'action_tier' in settings_keys:
        input_df['action_tier'] = input_df['action_tier'].map(action_rank_dict)

    
    crit_type_dict = {key: settings_dict[key]['type'] for key, value in settings_dict.items()}


    return input_df, crit_type_dict

def check_weights(settings_dict):
    """Performs some checks on the weights set in the settings.py file:
    
    1) Check to ensure total weights add up to 1
    2) Create a dict that has a one-on-one mapping of criteria and weights
    
    Args:
        settings_dict (dict): Dictionary containing the TOPSIS settings

    Returns:
        Dict: A one-on-one dictionary mapping the criteria to their assigned weights
    """


    # Check to see if weights are correctly distributed
    weights = [settings_dict[x]['weight'] for x in settings_dict.keys()]
    if round(sum(weights),2) != 1:
        logging.error(f"WEIGHTS CHECK FAILED: Sum of weights does not add up to 1: {sum(weights)}")
        quit()
    else:
        logging.info("WEIGHTS CHECK PASSED: Weights add up to 1")
    
    
    # Generate a weights only 1 on 1 dictionary.   
    weight_dict = {}
    for key in settings_dict.keys():
        weight_dict[key] = settings_dict[key]['weight']
        
    return weight_dict

def distribute_DBP_weights(input_df, settings_dict, DBP_dict, 
                           DBP_merged = False):
    """Distribute weights assigned to general DBP criteria over individual DBP
    type criteria.
    
    I.e., weight of 'positive_DBP' item is 0.5, and we have a ranked DBP dict = 
    {'THM': 1, 'HAA': 3, etc.}. The function will distribute the 0.5 over the
    DBP types such that they add up to 0.5 but are distributed according to the
    given ranking. 
    
    The individual DBP values are then added to the original settings dict, and
    the general DBP items removed. 

    Args:
        input_df (DataFrame): Dataframe containing the TOPSIS input data
        settings_dict (Dict): Contains the TOPSIS settings
        DBP_dict (Dict): Dict containing the ranking of the individual DBPs
        DBP_merged (bool, optional): Whether different DBP columns (i.e., 
        positive/negative/other) have been merged or not. Defauls to False

    Returns:
        Dict: Updated settings dict. 
    """
    if DBP_merged:
        dbp_column_start = ('all',)
    else:
        dbp_column_start = ("positive", "negative", "other")
    
    # Get available DBPs from data
    DBPs_in_data_lst = [x.split('_')[1] for x in input_df.keys() 
                        if x.startswith(dbp_column_start)]
    DBPs_in_data_lst = list(set(DBPs_in_data_lst))
    # Get DBPs with ranking
    DBPs_in_sett_lst = list(DBP_dict.keys())
    
    # Remove DBPs not in data from ranked DBPs
    DBPs_missing = [x for x in DBPs_in_sett_lst if x not in DBPs_in_data_lst]
    for dbp in DBPs_missing:
        DBP_dict.pop(dbp, None)
    
    # Recalculate the rankings such that they are assigned a weight (with highest
    # weight given to higher rank)

    # Step 1: Identify the range of the rankings
    max_rank = max(DBP_dict.values())

    # Step 2: Invert the rankings
    inverted_rankings = {key: (max_rank - rank + 1) for key, rank 
                         in DBP_dict.items()}

    # Step 3: Normalize the inverted rankings to a range from 0 to 1
    total_inverted = sum(inverted_rankings.values())
    normalized_rankings = {key: rank / total_inverted for key, rank 
                           in inverted_rankings.items()}

    # Step 4: Get weights assigned to DBP positive, negative and other effect
    # and multiply with normalized rankings

    for effect_type in dbp_column_start:
        new_rankings = {str(effect_type)+'_'+key: 
                        {'type': settings_dict[str(effect_type)+'_DBP']['type'], 
                        'weight': value*settings_dict[str(effect_type)+'_DBP']['weight']} 
                        for key, value in normalized_rankings.items()}
        # Add to rankings dict and removed general DBP category. 
        settings_dict.update(new_rankings)
        settings_dict.pop(str(effect_type)+'_DBP')
    
    # Return updated settings dictionary
    return settings_dict

def prep_data_for_TOPSIS(input_df, weight_dict, criteria_dict):
    """Prepare data for TOPSIS analysis by casting dataframe and dict values
    to numpy arrays
    
    Args:
        input_df (DataFrame): Pandas dataframe containing the input data
        weight_dict (Dict): Dictionary containing the weights for each column
        criteria_dict (Dict): Dictionary containing the criteria type for each 
        column (i.e., beneficial or detrimental)

    Returns:
        numpy arrays: The input data in numpy array format. 
    """
    
    # Create simple lists according to Dataframe column order
    weight_lst = []
    criteria_lst = []

    for key in input_df.keys():
        weight_lst.append(weight_dict[key])
        criteria_lst.append(criteria_dict[key])
    
    # Cast to numpy arrays
    weight_np = np.array(weight_lst)
    crit_type_np = np.array(criteria_lst)
    data_np = input_df.to_numpy(dtype=np.float64)

    # Return results
    return data_np, weight_np, crit_type_np
    
def do_TOPSIS(input_df, weight_dict, crit_type_dict):
    """Main function that carries out the TOPSIS analysis.
    
    Takes as input the data, the weights, and the criteria types and produces
    a ranking based on TOPSIS scores and similarity indexes.

    Args:
        input_df (DataFrame): Dataframe containing the data
        weight_dict (Dict): Dictionary containing the assigned weights
        crit_type_dict (Dict): Dictionary containing the criteria types
        
    Returns:
        DataFrame: A dataframe containing the final ranked actions.
    """
    
    # TOPSIS calculation inspired by 
    # https://www.kaggle.com/code/hungrybluedev/topsis-implementation/notebook
    
    # 0) Format TOPSIS input into numpy arrays/lists
    data_np, weight_np, crit_type_np = prep_data_for_TOPSIS(input_df, 
                                                            weight_dict, 
                                                            crit_type_dict)
    
    all_actions = np.array(input_df.index.to_series())
    
    # 1) Normalize ratings
    n_rows = len(data_np)
    n_columns = len(weight_np)
    
    divisors = np.empty(n_columns)
    for j in range(n_columns):
        column = data_np[:, j]
        divisors[j] = np.sqrt(column@column) # The '@' performs matrix multiplication
    
    data_np /= divisors
    
    # 2) Calculate weighted normalized ratings
    data_np *= weight_np
    
    # 3) Calculate best/worst possible alternatives
    a_pos = np.zeros(n_columns)
    a_neg = np.zeros(n_columns)
    for j in range(n_columns):
        column = data_np[:,j]
        max_val = np.max(column)
        min_val = np.min(column)
    
        # See if we want to maximize benefit or minimize cost
        if crit_type_np[j] == 1: # Where higher value is better
            a_pos[j] = max_val
            a_neg[j] = min_val
        elif crit_type_np[j] == -1: # Where lower value is better
            a_pos[j] = min_val
            a_neg[j] = max_val

    # 4) Calculating seperation measures and topsis score of best/worst 
    # alternatives for each of the actions
    sp = np.zeros(n_rows)
    sn = np.zeros(n_rows)
    cs = np.zeros(n_rows)

    for i in range(n_rows):
        diff_pos = data_np[i] - a_pos
        diff_neg = data_np[i] - a_neg
        sp[i] = np.sqrt(diff_pos @ diff_pos)
        sn[i] = np.sqrt(diff_neg @ diff_neg)
        denom = sp[i] + sn[i]
        cs[i] = sn[i] / denom if denom != 0 else 0

    # 5) Rank according to seperation measures and topsis scores
    def rank_according_to(data, actions):
        ranks = rankdata(data).astype(int)
        ranks -= 1
        # Sort according to rank
        ind = np.argsort(ranks)
        ranks = ranks[ind]
        actions = actions[ind][::-1]
        return actions
    
    cs_order = rank_according_to(cs, all_actions)
    sp_order = rank_according_to(sp, all_actions)
    sn_order = rank_according_to(sn, all_actions)

    # Create the final ranked dataframe
    ranked_df = pd.DataFrame(data=zip(cs_order, sp_order, sn_order), 
                             index=range(1, n_rows + 1), 
                             columns=["Score", "Splus", "Sminus"])
    
    # Save the final ranked dataframe to an excel file
    # folder_name = out_dir.split('/')[-2]
    # output_name = out_dir + folder_name + "_TOPSIS-result-ranked.xlsx"
    # #ranked_df.to_excel(output_name)
    # logging.info(f"Ranked actions saved as '{output_name}'")
    logging.info("Ranked actions returned as DataFrame")
    # Return the final ranked dataframe
    return ranked_df
      


# def main():
        
#     # Load settings

#     weight_settings = {"all_DBP": {"type": 1,"weight": 0.428},"cost_tier": {"type": 1,"weight": 0.142},"time_tier": {"type": 1,"weight": 0.215},"repeat_tier": {"type": 1,"weight": 0.215}}

#     DBP_ranking_dict = {
#         "THM": 1,
#         "IDBP": 1,
#         "BrDBP": 1,
#         "HAA": 2,
#         "HAN": 3,
#         "CB": 4,
#         "NS": 5,
#         "HAL": 6,
#         "HAM": 7,
#         "HNM": 8,
#         "HBQ": 9,
#         "PDBP": 10,
#         "HP": 11,
#         "BPA": 12,
#         "VOC": 12,
#         "HDBP": 12,
#         "AOX": 12
#     }

    
#     action_cat_ranking_dict = {
#         "RW": 1,
#         "CA": 1,
#         "PN": 1,
#         "PC": 1,
#         "FL": 1,
#         "BL": 1,
#         "CK": 1,
#         "A_other": 1
#     }

    
#     dec_matrix_settings = {
#         "input_file": "./input/input_data_topsis_IQR_merge-DBP_all-DBP.xlsx",
#         "cost_time_setting": "IQR",
#         "collect_DBP": "all-DBP"
#     }

#     # Load data file
#     input_filename = dec_matrix_settings['input_file']

#     input_data_df = pd.read_excel(input_filename,index_col = [0])
#     input_data_df = input_data_df.drop(columns=["all_Other"], errors="ignore")
    
#     logging.info(f"Starting TOPSIS run: {"expert-weights"}")
    
#     # Check the data for zero columns (i.e., all entries zero)
#     input_data_df = check_data(input_data_df, map_acronyms = False)
    
#     # Set DBP weight distributions
#     weight_settings = distribute_DBP_weights(input_data_df, weight_settings, 
#                                              DBP_ranking_dict, 
#                                              DBP_merged = True)
    
#     # Check settings for criteria
#     input_data_df, crit_type_dict = check_criteria(input_data_df, 
#                                                    weight_settings, 
#                                                    action_cat_ranking_dict)
#     for col in input_data_df.columns:
#         if col not in weight_settings:
#             logging.warning(f"⚠️ Column '{col}' not found in weight settings!")


#     # Check settings for weights and retrieve direct weights dictionary
#     weight_dict = check_weights(weight_settings)
    


#     # Do TOPSIS
#     out_df = do_TOPSIS(input_data_df, weight_dict, crit_type_dict)
#     print(out_df)

#     logging.info("Finished TOPSIS run.")
    
# if __name__ == "__main__":
#     main()
