import logging, os





def DownloadFASTQs(dfu, fastq_ref_list, output_dir):
    """
    dfu: DataFileUtil Object
    fastq_ref_list: (list<s>) list of refs 'A/B/C' A,B,C are integers
    output_dir: (s) Path to scratch directory or tmp_dir
    """
    fastq_fp_l = []


    for i in range(len(fastq_ref_list)):
        crnt_fastq_ref = fastq_ref_list[i]
        logging.critical("crnt fq ref: " + crnt_fastq_ref)
        #Naming and downloading fastq/a file using DataFileUtil
        fastq_fn = "FQ_" + str(i)
        fastq_fp = os.path.join(output_dir, fastq_fn)
        get_shock_id_params = {"object_refs": [crnt_fastq_ref], "ignore_errors": False}
        get_objects_results = dfu.get_objects(get_shock_id_params)

        # We should try to get file name from Get Objects Results
        fq_shock_id = get_objects_results['data'][0]['data']['lib']['file']['id']
        fastq_download_params = {'shock_id': fq_shock_id,'file_path': fastq_fp, 'unpack':'unpack'}
        #Here we download the fastq file itself:
        logging.info("DOWNLOADING FASTQ FILE NUMBER " + str(i+1))
        file_info = dfu.shock_to_file(fastq_download_params)
        logging.info(file_info)
        fastq_fp_l.append(fastq_fp)

    return fastq_fp_l



# Deprecated
def download_fastq(dfu, fastq_refs_list, scratch_dir, output_fp):
    # We get multiple shock objects at once.
    get_shock_id_params = {"object_refs": fastq_refs_list, 
            "ignore_errors": False}
    get_objects_results = dfu.get_objects(get_shock_id_params)
    logging.debug(get_objects_results['data'][0])
    logging.debug(len(get_objects_results['data']))
    
    # We want to associate a ref with a filename and get a dict that has this
    # association

    raise Exception("STOP - INCOMPLETE")
    fq_shock_id = get_objects_results['data'][0]['data']['lib']['file']['id']
    fastq_download_params = {'shock_id': fq_shock_id,'file_path': fastq_fp, 'unpack':'unpack'}
    #Here we download the fastq file itself:
    logging.info("DOWNLOADING FASTQ FILE " + str(i))
    file_info = dfu.shock_to_file(fastq_download_params)
    logging.info(file_info)
