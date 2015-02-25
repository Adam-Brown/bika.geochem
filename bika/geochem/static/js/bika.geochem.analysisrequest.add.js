/**
 * Controller class for AnalysisRequest add view
 */
function GeochemAnalysisRequestAddView() {

    var that = this;

    // ------------------------------------------------------------------------
    // PUBLIC ACCESSORS
    // ------------------------------------------------------------------------


    // ------------------------------------------------------------------------
    // PUBLIC FUNCTIONS
    // ------------------------------------------------------------------------

    this.load = function() {

        // ------------------------------------------------------------------------
        //  Entry-point method for AnalysisRequestAddView
        // ------------------------------------------------------------------------
        columns = parseInt($('input#ar_count').val());
        for (i = 0; i < columns; i++) {
            var igsnInputField = $('input#IGSN-' + i);

            // Remove the old validator:
            igsnInputField.off('blur');

            // Add the new lookup function:
            igsnInputField.blur(igsnLookup);
        }

    };

    // ------------------------------------------------------------------------
    // PRIVATE FUNCTIONS
    // ------------------------------------------------------------------------

    function igsnLookup(event) {

        entered_value = $(this).val();
        if (entered_value.match(/^[a-zA-Z]{5}[0-9a-zA-Z]{4}$/)) {

            if (this.lastlookup != entered_value) {

                this.lastlookup = entered_value;

                $.ajax({
                        url: "/igsn-lookup/lookup.php?igsn_url=http://app.geosamples.org/sample/igsn/" + entered_value,
                        context: document.body
                    }).done(function(response) {
                        // This just pulls out the -0 from IGSN-0 so we can work out which column we're in.
                        column_number = $(event.target).attr('id').replace(/^(.+)([0-9]+)$/, '$2');

                        //console.log('Value of IGSN' + column_number);
                        //console.log(response);

                        $('#SampleName-' + column_number).val(response['Sample Name']);
                        $('#SampleType-' + column_number).val(response['Sample Type']);
                        $('#Latitude-' + column_number).val(response['Latitude']);
                        $('#Longitude-' + column_number).val(response['Longitude']);
                    });
            }
        }
    }
}
