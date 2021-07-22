import os, logging



def prepare_outputs(dfu, HTML_fp, html_dir,
                    csv_fp, csv_dir):
    """
    Args:
        dfu (KBase Class): DataFileUtil object
        HTML_fp (str): Path to HTML file of csv
        html_dir (str): Path to dir containing HTML file (Inside workdir)
        csv_fp (str): Path to CSV file
        csv_dir (str): Path to dir containing CSV file (Inside workdir)
    """


    # Returning file in zipped format:-------------------------------
    file_zip_shock_id = dfu.file_to_shock({'file_path': csv_dir,
                                          'pack': 'zip'})['shock_id']

    dir_link = {
            'shock_id': file_zip_shock_id, 
           'name':  'results.zip', 
           'label':'find_tsp_model_output_dir', 
           'description': 'The output directory from ' \
            + 'Find Transposon Model.'
    }
    
    # Preparing HTML output
    HTML_report_shock_id = dfu.file_to_shock({
            "file_path": html_dir,
            "pack": "zip"
            })['shock_id']

    HTML_report_d_l = [{"shock_id": HTML_report_shock_id,
                        "name": os.path.basename(HTML_fp),
                        "label": "Find Transposon Model Results",
                        "description": "HTML Summary Report for Find Transposon Model app."
                        }]

    report_params = {
            "html_links": HTML_report_d_l,
            "direct_html_link_index": 0,
            "html_window_height": 333,
            "message": "Finished Running Find Transposon Model"
    }

    report_params["file_links"] = [dir_link]

    return report_params




