# We make sure the parameters are right



import logging
import os


def validate_params(params):
    
    for x in ["fastq_ref_list", "maxReads", "minQuality"]:
        if x not in params:
            raise Exception(f" {x} must be part of params."
                            " Params: " + ", ".join(params.keys()))

    if params["maxReads"] is None or params["maxReads"] == "":
        params["maxReads"] = 600000
    if params["minQuality"] is None or params["minQuality"] == "":
        params["minQuality"] = 10

    for x in ["maxReads", "minQuality"]:
        if isinstance(params[x],str):
            if "," in params[x]:
                params[x] = params[x].replace(",","")
            params[x] = int(params[x])

    if not isinstance(params["minQuality"], int):
            raise Exception(f"Param minQuality must be passed as an int."
                            f" Currently {type(params['minQuality'])}.")

    if not len(params["fastq_ref_list"]) > 0:
        raise Exception(f"There must be at least one fastq file to check. The program recognizes none.")


    return None


def o_stop(val):
    raise Exception(f"Stopping: {str(val)}")

