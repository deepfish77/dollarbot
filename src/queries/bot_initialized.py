import json
from src.utils.rds_instance import get_rds_instance as rds_connector


def get_commitments_for_user(user_id, to_external=True):

    query = f"""SELECT * from users.commitments where user_id = '{user_id}'"""
    try:
        results_df = rds_db.get_records_into_df(query)
        cleaned_json_dict = set_results_for_single_item_response(results_df=results_df)
        return cleaned_json_dict if to_external else results_df

    except Exception as e:
        print("cannt get commitment for user", e)
        return {"failed to get the commitment for user ": e}
