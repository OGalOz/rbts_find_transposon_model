







def convert_dataframe_into_HTML_file(result_df, html_fp):
    """
    Args:
        result_df (pandas DataFrame): Columns are
            index (model_name, (str)): The model's name
            nReads (int): Total number of reads from FASTQ file
            nModelStartFound (int): Number of reads with start of model found
            nModelEndFound (int): Number of reads with end of model found
            start_frac (float):  nModelStartFound/nReads
            end_frac (float):  nModelEndFound/nReads
        html_fp (str): Path to output HTML file to 
    Description:
        We take the dataframe with results and create an HTML file to view
    """
    html_str = result_df.to_html()
    with open(html_fp, 'w') as g:
        g.write(html_str)
