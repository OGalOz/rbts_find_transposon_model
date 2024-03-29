/*
A KBase module: rbts_find_transposon_model
*/

module rbts_find_transposon_model {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_rbts_find_transposon_model(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
