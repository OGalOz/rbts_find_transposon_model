# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import subprocess
import json
import shutil
import pandas as pd

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace
from mapts_util.ModelTestMapTnSeq import FindWorkingModel
from mapts_util.validate import validate_params, o_stop
from mapts_util.downloader import DownloadFASTQs
from mapts_util.PrepareOP import prepare_outputs
from mapts_util.HTMLReport import convert_dataframe_into_HTML_file 

#from Bio import SeqIO
#from full.FullProgram import CompleteRun
#from util.PrepareIO import PrepareProgramInputs, PrepareUserOutputs



#END_HEADER


class rbts_find_transposon_model:
    '''
    Module Name:
    rbts_find_transposon_model

    Module Description:
    A KBase module: rbts_find_transposon_model
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.ws_url = config['workspace-url']
        #END_CONSTRUCTOR
        pass


    def run_rbts_find_transposon_model(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
            genome_ref
            gene_table_ref
            fastq_ref_list
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
    
        
        What do we take as inputs?
            FASTQ files
            Genome FNA (?) - maybe we don't even use this.
        What do we need?
            All the existing possible 'models' to check FASTQs against.
        What do we do?
            For each fastq file (Or only the first) - check how many reads
            hit a given model. Keep a dict with how many reads were hit.
            Do this for each model. Compare all the models at the end.
            Create an HTML report file describing the results of the
            different models on the FASTQ files.
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_rbts_find_transposon_model
     
        logging.basicConfig(level=logging.DEBUG)
        

        # PREPARE PARAMS
        validate_params(params) 


        dfu = DataFileUtil(self.callback_url)
        #gfu = GenomeFileUtil(self.callback_url)
        # We need the workspace object to get info on the workspace the app is running in.
        token = os.environ.get('KB_AUTH_TOKEN', None)
        ws = Workspace(self.ws_url, token=token)
        ws_info = ws.get_workspace_info({'workspace': params['workspace_name']})
        workspace_id = ws_info[0]
        # FIXED LOCATIONS ----------
        td = self.shared_folder
        models_dir = "/kb/module/lib/rbts_find_transposon_model/models"
        cfg_fp = "/kb/module/lib/mapts_util/mts_cfg.json"
        fastqs_dir = os.path.join(td, "FASTQs")
        os.mkdir(fastqs_dir)
        op_dir = os.path.join(td, "results")
        os.mkdir(op_dir)
        html_dir = os.path.join(td, "HTML")
        os.mkdir(html_dir)


        # Functions ----------
        # Downloading fastq files:
        DownloadFASTQs(dfu, params['fastq_ref_list'], fastqs_dir)
        # For now using only one fastq file
        fastq_fp = os.path.join(fastqs_dir, os.listdir(fastqs_dir)[0])

        # Getting config dict
        with open(cfg_fp, 'r') as f:
            cfg_d = json.loads(f.read())
            cfg_d['maxReads'] = params["maxReads"]
            cfg_d['minQuality'] = params["minQuality"]
        model_results_list = FindWorkingModel(fastq_fp, models_dir, cfg_d)
        logging.debug(model_results_list)

        # Creating dataframe----
        # First initialize the dataframe dict
        pre_df_dict = {k:[] for k in model_results_list[0].keys()}
        # Now we populate the lists of the dict
        for res_d in model_results_list:
            for k in res_d.keys():
                pre_df_dict[k].append(res_d[k])
        # Here we create the dataframe from the dict
        model_res_df = pd.DataFrame.from_dict(pre_df_dict)
        model_res_df.index = model_res_df["model_name"]
        # Sort it in decreasing by start_frac and end_frac
        model_res_df.sort_values(by=["start_frac", "end_frac"], 
                                inplace=True,
                                ascending=False)
        logging.info(model_res_df)
        CSV_op_fp = os.path.join(op_dir, "Find_Transposon_Model_Results.csv")
        model_res_df.to_csv(CSV_op_fp, index=False)

        HTML_op_fp = os.path.join(html_dir, "Find_Transposon_Model_Results_Table.html")
        convert_dataframe_into_HTML_file(model_res_df, HTML_op_fp)
        report_params = prepare_outputs(dfu, HTML_op_fp, html_dir, CSV_op_fp, op_dir)
        report_params["workspace_name"] = params["workspace_name"]


        report_util = KBaseReport(self.callback_url)
        report_info = report_util.create_extended_report(report_params)

        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_rbts_find_transposon_model

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_rbts_find_transposon_model return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
