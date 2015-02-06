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

    function igsnLookup() {
        $.ajax({
				url: "/igsn-lookup/lookup.php?igsn_url=http://app.geosamples.org/sample/igsn/" + $(this).val(),
				context: document.body
			}).done(function(response) {
			    console.log('Value of ' + $(this).attr('id') + " = " + response)
			});
    }
}
