import json


def _remove_slashes(obj):
    if isinstance(obj, str):
        return obj.replace("/", "")
    return obj


def set_results_json_api_resp(results_df,orient="records"):

    json_results = results_df.to_json(orient=orient)
    cleaned_json_dict = json.loads(json_results, object_hook=_remove_slashes)
    return cleaned_json_dict


def set_results_for_single_item_response(results_df):
    return json.loads(results_df.iloc[0].to_json())