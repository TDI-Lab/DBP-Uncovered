"""
Python file containing the acronym dictionary, linking all acronyms to their
full meaning. Can be imported into other scripts
"""
import pycountry

# Dict that has meaning of all countries
iso_country_codes_dict = {country.alpha_2: country.name for country in pycountry.countries}
iso_country_codes_dict_a2_a3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}

iso_alpha2_list = list(iso_country_codes_dict.keys()) + ["XX"]

direct_acronym_meaning_dict = {
   # Actions (first acronym is general catergory)
    'RW': 'Reduce waste',
    'CA': 'Cleaning',
    'PN': 'Plumbing',
    'PC': 'Personal care',  
    'FL': 'Filtering',
    'FL_mtn': 'Filter maintenance',    
    'BL': 'Boiling',   
    'CK': 'Kitchen', 
    
    # 'RW': 'Reduced waste/pollution',
    'LP': 'Recycle plastics correctly',
    'RC': 'General recycling',
    'DPh': 'Dispose (old) pharmaceuticals correctly',
    'DBPA': 'Dispose of BPA products correctly',
    'DPCP': 'Dispose (old) personal-care products correctly',
    'DCP': 'Dispose (old) cleaning products correctly',
    'DF': 'Dispose food correctly',
    'nAg': 'Avoid products containing nano-silver',
    'IR': 'Avoid use of insect repellants in non-ventilated spaces',
    'RD': 'Use recommended dosages of household products', 
    # detergents, shampoos, etc. 
    
    #'CA': 'Cleaning activities',   
    'VLM': 'Ventilate washing machine after usage',
    'BP': 'Switch to a bleach alternative',
    'BPAP': 'Avoid BPA-containing products',
    'VC': 'Increase ventilation while cleaning',
    'WLT': 'Wash at lower temperatures',
    
    #'PN': 'Plumbing network',    
    'PM': 'Change pipe materials',
    'FP': 'Flush pipes before use when not used regularly',
    'hW': 'Harden water',
    
#   'PC': 'Personal care',  
    'SS': 'Ventilate between successive showers',
    'IV': 'Improve bathroom ventilation',
    'RST': 'Reduce shower time',
    'PCBPA': 'Avoid use of personal care products containing BPA',
    
    # 'FL': 'Filtering device',
    'AC': 'Activated carbon',
    'MT': "Membrane technologies",
    'PP': "Polypropylene filters",
    'AC_IER': 'Combination of activated carbon and ion-exchange resins',
    'AC_MT': 'Combination of activated carbon and membrane technology',
    'FL_CT': 'Other combination of filter technologies',
    'Other_FL': 'Other filtering device type',
    
    # 'FL_mtn': 'Filter maintenance', 
    'RF': 'Replace filter cartridge regularly',
    
    # 'BL': 'Boiling activity',   
    'STO': 'Boil water on the stove (open lid)',
    'STC': 'Boil water on the stove (closed lid)',
    'DU': 'Distillation unit',
    'BD': 'Use a boiling device (e.g., kettle)',
    'MI': 'Boil water in microwave',
    'STOplus': 'Boil water on the stove (open lid + addition of ascorbate/carbonate)',
    'WB': 'Boil water using a water bath',
    'Unclear_BL': 'Unclear boiling process',
    'IBL': 'Use an instant boiling water unit', 

    #'CK': 'Cooking activities',    
    'IG': 'Soak iodine-containing ingredients before use',
    'NaCl': 'Choose salts without iodine',
    'WS': 'Store water in a clay pot',
    'PSS': 'Pouring/stirring/shaking before consumption',
    'BR': 'Use open lid when brewing coffee/tea',
    'RFW': 'Refrigerate water before consumption',
    'SWO': 'Store water open before consumption', 
    'BLS': '(Brewing) artifical sweetener instead of sugar',
    'LCT': '(Salt) long cooking time',
    'HCT': '(Salt) high cooking temperature',
    
    # Other action type
    'VN': 'Ventilation',
    'AirC': 'Air conditioning',
    'BW': 'Bottled water',
    'CoI': 'Communication of issues'
}

direct_keyword_meaning_dict = {
    'reduce-waste': 'Reduce waste', 
     'cleaning': 'Cleaning action', 
     'plumbing': 'Plumbing action', 
     'bathroom': 'Personal care', 
     'filtering': 'Filtering action', 
     'boiling': 'Boiling', 
     'kitchen': 'Kitchen action', 
     'recycle-plastics': 'Recycle plastics',
     'recycle-general': 'Recycle general',
     'dispose-pharma-corr': 'Dispose pharmaceuticals correctly',
     'dispose-BPA-corr': 'Dispose of BPA products correcty', 
     'dispose-personal-care-corr': 'Dispose personal care products correctly',
     'dispose-cleaning-prod-corr': 'Dispose cleaning products correctly', 
     'dispose-food-correctly': 'Dispose food items correctly', 
     'avoid-nanosilver-product': 'Avoid products containing nanosilver', 
     'avoid-insectrepellant-inside': 'Avoid use of insect repellant in enclosed spaces', 
     'use-recommended-prod-dose': 'Use recommended dosage of household products', 
     'ventilate-washing-machine': 'Ventilate washing machine after usage', 
     'use-bleach-alternative': 'Switch to bleack alternative', 
     'avoid-BPA-product': 'Avoid products containing BPA', 
     'increase-cleaning-vent': 'Increase ventilation while cleaning',
     'wash-clothes-lowT': 'Wash clothes at lower temperatures', 
     'change-plumbing-material': 'Change plumbing material',
     'flush-pipes-regularly': 'Flush pipes semi-regularly to avoid stagnation', 
     'harden-water': 'Harden water', 
     'ventilate-between-showers': 'Ventilate between successive showers',
     'increase-bathroom-vent': 'Increase bathroom ventilation', 
     'reduce-shower-length': 'Reduce shower length',
     'avoid-BPA-personal-care': 'Avoid use of personal care products containing BPA',
     'use-actcarbon-filter': 'Use activated carbon filter', 
     'use-membrane-filter': 'Use membrane technology filter',
     'use-polyprop-filter': 'Use polypropylene filter', 
     'use-distil-unit': 'Use distillation unit', 
     'use-actcarbon-ionexch-filter': 'Use filter with activated carbon and ion-exchange resin',
     'use-actcarbon-membrane-filter': 'Use filter with activated carbon and membrane technology',
     'use-othercomb-filter': 'Use other combination filter', 
     'replace-filter-cartridge': 'Replace filter cartridge regularly', 
     'boil-stove-open': 'Boil water on stove with an open lid', 
     'boil-stove-closed': 'Boil water on stove with closed lid',
     'boil-kettle': 'Use boiling device', 
     'boil-microwave': 'Use microwave for boiling', 
     'boil-instant-boiling-unit': 'Use instant boiling water unit', 
     'boil-water-bath': 'Boil water using a water bath', 
     'boil-stove-open-add-asccarb': 'Boil water on the stove (open lid + addition of ascorbate/carbonate)', 
     'boil-unclear': 'Unclear boiling device', 
     'soak-iodine-ingredients': 'Soak iodine-containing ingredients before use', 
     'avoid-iodine-salts': 'Avoid salts containing iodine', 
     'store-water-clay': 'Store water in a clay pot',
     'pour-stir-shake-drink': 'Pour/stir/shake beverage before consumption', 
     'brew-beverage-open': 'Use open lid when brewing coffee/tea', 
     'salt-cook-longer': 'Use longer cooking time when using salt',
     'salt-cook-hotter': 'Use higher cooking tempeture when using salt', 
     'increase-house-ventilation': 'Increase household ventilation', 
     'switch-air-cond': 'Switch to different air conditioning', 
     'refrigerate-water': 'Refrigerate water before consumption', 
     'store-water-open': 'Store water in an open container before use',
     'use-artif-sweet': 'Use artificial sweetener instead of sugar'
}


direct_acronym_keyword_dict = {
    # Keyword
    'RW': 'reduce-waste', 
    'CA': 'cleaning', 
    'PN': 'house/plumbing', 
    'PC': 'bathroom', 
    'FL': 'filtering', 
    'BL': 'boiling', 
    'CK': 'kitchen', 
    'LP': 'recycle-plastics', 
    'RC': 'recycle-general', 
    'DPh': 'dispose-pharma-corr', 
    'DBPA': 'dispose-BPA-corr', 
    'DPCP': 'dispose-personal-care-corr', 
    'DCP': 'dispose-cleaning-prod-corr', 
    'DF': 'dispose-food-correctly', 
    'nAg': 'avoid-nanosilver-product', 
    'IR': 'avoid-insectrepellant-inside', 
    'RD': 'use-recommended-prod-dose', 
    'VLM': 'ventilate-washing-machine', 
    'BP': 'use-bleach-alternative', 
    'BPAP': 'avoid-BPA-product', 
    'VC': 'increase-cleaning-vent', 
    'WLT': 'wash-clothes-lowT', 
    'PM': 'change-plumbing-material', 
    'FP': 'flush-pipes-regularly', 
    'hW': 'harden-water', 
    'SS': 'ventilate-between-showers', 
    'IV': 'increase-bathroom-vent', 
    'RST': 'reduce-shower-length', 
    'PCBPA': 'avoid-BPA-personal-care', 
    'AC': 'use-actcarbon-filter', 
    'MT': 'use-membrane-filter', 
    'PP': 'use-polyprop-filter', 
    'DU': 'use-distil-unit', 
    'AC_IER': 'use-actcarbon-ionexch-filter', 
    'AC_MT': 'use-actcarbon-membrane-filter', 
    'FL_CT': 'use-othercomb-filter', 
    'RF': 'replace-filter-cartridge', 
    'STO': 'boil-stove-open', 
    'STC': 'boil-stove-closed', 
    'BD': 'boil-kettle', 
    'MI': 'boil-microwave', 
    'IBL': 'boil-instant-boiling-unit', 
    'WB': 'boil-water-bath', 
    'STOplus': 'boil-stove-open-add-asccarb', 
    'Unclear_BL': 'boil-unclear', 
    'IG': 'soak-iodine-ingredients', 
    'NaCl': 'avoid-iodine-salts', 
    'WS': 'store-water-clay', 
    'PSS': 'pour-stir-shake-drink', 
    'BR': 'brew-beverage-open', 
    'LCT': 'salt-cook-longer', 
    'HCT': 'salt-cook-hotter', 
    'VN': 'increase-house-ventilation', 
    'AirC': 'switch-air-cond', 
    'RFW': 'refrigerate-water', 
    'SWO': 'store-water-open', 
    'BLS': 'use-artif-sweet'
}

direct_acronym_other = {
    # General
    'Other': 'Other',
    'NoAp': 'Unknown',
    'Yes': 'Yes',
    'No': 'No',
    'NoCh': 'No change',
    
    # DBP specific
    'THM': 'Trihalomethanes',
    'HAA': 'Haloacetic acids',
    'HAL': 'Haloacetaldehydes',
    'HNM': 'Halonitromethanes',
    'HAM': 'Haloacetamides',
    'HBQ': 'Halobenzoquinones',
    'HAN': 'Haloacetonitriles',
    'CB': 'Chlorites/chlorates/bromates',
    'NS': 'N-Nitrosamines',
    'IDBP': 'Iodinated DBPs',
    'PDBP': 'Phenolic DBPs',
    'BrDBP': 'Brominated DBPs',
    'BPA': 'BPA and its DBPs',
    'HP': 'Halophenols',
    'PPCP': 'Pharmaceutical/PCP specific DBPs',
    'TOX' : 'Total organic halides',
    'AOX': 'Adsorbable organic halogens',
    'VOC': 'Volatile organic compounds',
    'GPL': 'General pollutants',
    'HDBP': 'General halogenated DBPs',
    'nHDBP': 'General non-halogenated DBPs',
    
    # Study type
    'TX': 'Toxicology',
    'EXP': 'Exposure assessment',
    'ENV': 'Environment',
    'CH': 'Chemical',
    'WTu': 'Water utility treatment',
    'WTh': 'Water treatment at home',
    'LC': 'Life-cycle analysis',
    'RV': 'Review',
    'SIM': 'Simulations',
    
    # Action proposal type
    'AS': 'Measured',
    'AP': 'Proposed',
    'AI': 'Inferred',
    
    # Residual disinfectant
    'Cl': 'Chlorine',
    'Ca': 'Chloramine',
    'oCa': 'Organic chloramine',
    'ClO2': 'Chlorine dioxide',
    'Oz': 'Ozonation',
    'UV': 'UV exposure',
    'Syn': 'Synthetic DBPs',
    'D_other': 'Other disinfectant',
    
 
    # Action repeat
    'DW': 'Daily/weekly',
    'YD': 'Yearly/decadely',
    'OT': 'One-time change',
    
    # Action beneficiary
    'HHs': 'Human health self',
    'HHo': 'Human health others',
    
    # Action efficiency
    'plus': 'Measured change',
    'min': 'No measured change',
    'dep': 'Change dependent',
    
    # Action effect
    'pos': 'DBPs -',
    'neg': 'DBPs +',
    'dot': 'Effect depends on DBP',
    'doa': 'Effect depends on combined action',
    'inc': 'Inconclusive',
    
    'Ya': 'Yes, active',
    'Yp': 'Yes, passive',
    'N': 'No',
    
    # Bias assesment
    'OD': 'Open data',
    'POD': 'Partially open data',
    'NOD': 'No open data'
}


direct_acronym_keyword_dict.update(direct_acronym_other)
direct_acronym_meaning_dict.update(direct_acronym_other)
direct_keyword_meaning_dict.update(direct_acronym_other)


# Possible actions
# Key/item is 'Action_type_I' and 'Action_type_II'
action_types_dict = {
    'RW': ["LP", "RC", "DPh", "DPCP", "DHP", "DBPA", "DCP", "DF", "nAg", "RD"],
    'CA': ["CWm", "CWh", "CP", "MS", "BP", "BPAP", "KWm", 
        "VLM", "VDW", "KWh", "VC", "IR", "WLT"],
    'PN': ["PM", "TM", "FP", "GI", "sW", "hW", "VN", "AirC", "BW", "CoI"],
    "PC": ["WA", "SS", "IV", "RST", "PCBPA", "IR"],
    "FL": ["AC", "MT", "PP","Other_FL", "FL_CT", "AC_IER",
        "AC_MT", "RF"],
    "BL": ["STO", "STO+","STOplus", "STC", "BD", "MI", "WB", "IBL", "DU", "Unclear_BL"],
    "CK": ["IG", "NaCl", "LCT", "HCT", "WS", "RFW", "PSS", "BR", "BLS", "SWO"]
}


# Valid options for each dimension
valid_dim_entry_dict = {
    'DBP_type': ["THM", "HAA", "HAN", "HAM", "HNM", "HAL","HBQ", "CB", "NR", 
                 "IDBP", "NS", "PDBP", "BrDBP", "HDBP", "nHDBP", "BPA", "PPCP", 
                 "TOX", "AOX", "VOC",  "NoAp", "GPL", "HP", "Other"],
    'Study_type': ["TX", "EXP", "SIM", "ENV", "CH", "LC", "WTu", "WTh", "Art_Other", 
                   "RV"],
    'Action_proposal_type': ["AS", "AP", "AI"],
    'Disinfectant_type': ["Cl", "Ca", "oCa", "Oz", "ClO2", "UV", "Syn",
                            "D_other", "NoAp"],
    'Action_type_I': ["RW",  "CA", "PN", "PC", "FL", "BL", "CK", "A_Other", "Other"],
    'Action_repeat': ["DW", "YD", "OT"],
    'Action_beneficiary': ["DE", "IE", "Both", "Other"],
    'Action_efficiency': ["plus", "min", "dep", "NoAp"],
    'H_Participation': ["Yp", "Ya","N"],
    'Country': iso_alpha2_list,
    'CoI_statement': ["Yes", "No", "NoAp"],
    'Open_data': ["OD", "POD", "OD", "NoAp", "NOD"],
    'Action_type_II': ["LP", "RC", "DPh", "DPCP", "DHP", "DBPA", "DCP", "DF", 
                       "nAg", "RD", "CWm", "CWh", "CP", "MS", "BP", "BPAP", "KWm", 
                        "VLM", "VDW", "KWh", "VC", "IR", "WLT", "PM", "TM", "FP", 
                        "GI", "sW", "hW", "WA", "SS", "IV", "RST", "PCBPA", 
                        "AC", "MT", "DU", "PP","Other_FL", "FL_CT", "AC_IER",
                        "AC_MT", "RF", "STO", "STOplus", "STC", "BD", "MI", "WB", 
                       "IBL", "Unclear_BL", "IG", "NaCl", "LCT", "HCT", "WS", "RFW", 
                        "PSS", "BR", "BLS", "SWO", "VN", "AirC", "BW", "CoI"],
    'Action_effect': ["pos", "neg", "dot", "doa","inc", "NoCh", "NoAp"],
    'Action_cost': ['>100', '10-100', '0-10', 'NoAp']
}


full_dimension_name_dict = {
    'DBP_type': 'DBP family',
    'Study_type': 'Field of study',
    'Action_proposal_type': 'Action study type',
    'Disinfectant_type': 'Residual disinfectant',
    'Action_type_I': 'Action category I',
    'Action_type_II': 'Action category II',
    'Action_repeat': 'Action repetition',
    'Action_beneficiary': 'Goal of action',
    'Action_efficiency': 'Action efficiency',
    'Action_effect': 'Action effect',
    'Action_effect_.-DBP_type_.': 'Action_effect',
    'Action_cost': 'Action_cost',
    'H_Participation': 'Human subjects',
    'Country': 'Country',
    'CoI_statement': 'Conflict of interest',
    'Open_data': 'Open data',
    'publication_year': 'Year of publication'
}


# Expand dictionaries by including all possible combinations?
# Currently not in use. 
do_combinations = False
if do_combinations:
    combo_lists = ['Action_type_I', 'Action_type_II']

    for list in combo_lists:
        
        valid_entries = valid_dim_entry_dict[list]
        new_valid_entries = []
        for entry1 in valid_entries:
            for entry2 in valid_entries:
                new_valid_entries.append(entry1+'+'+entry2)
                new_valid_entries.append(entry2+'+'+entry1)
        
        valid_entries = valid_entries + new_valid_entries
        
        valid_dim_entry_dict[list] = valid_entries
        
        