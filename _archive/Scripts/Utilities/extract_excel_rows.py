import pandas as pd
import json
import traceback

file_path = "01_Raw/ML/Poscobro/1 enero 2026 - 1 mayo 2026.xlsx"
try:
    df = pd.read_excel(file_path, engine="calamine")

    # The user wants to audit 13 specific records.
    # The records have operation_id in the form: POS_{CHL_id}_..._{row_number}
    # Wait, in the database I saw operation_id values like:
    # POS_146992054084_1 enero 2026 - 1 mayo 2026.xlsx_1385
    # The number at the end is likely the row number from the DB pipeline.
    # We can also just search by the CHL_id (e.g. 146992054084) or the order_id (e.g. 2000015218717874)

    target_order_ids = ['2000015218717874', '2000015208258540']
    target_chl_ids = [
        '145894070480', '145201714585', '145196331393', '146992693700', 
        '147238582019', '144667518268', '146704890456', '144623804641', 
        '144390458215', '147972369944', '145404934728'
    ]

    evidence = []

    for idx, row in df.iterrows():
        row_dict = {k: str(v) for k, v in row.items()}
        # search the row strings for the identifiers
        row_str = " ".join([str(v) for v in row.values])
        
        match = False
        for oid in target_order_ids:
            if oid in row_str:
                match = True
                row_dict['_match_type'] = 'Ajuste Poscobro Conciliado'
                break
        
        if not match:
            for cid in target_chl_ids:
                if cid in row_str:
                    match = True
                    row_dict['_match_type'] = 'Ajuste Poscobro General'
                    break
                    
        if match:
            evidence.append(row_dict)

    with open("poscobro_evidence.json", "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(evidence)} records successfully!")
except Exception as e:
    print("Error:")
    traceback.print_exc()
