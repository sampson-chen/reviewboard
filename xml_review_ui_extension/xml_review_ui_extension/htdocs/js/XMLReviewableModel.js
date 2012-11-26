alert("Model Loading");

/*
 * Provides review capabilities for XML files.
 */
RB.XMLReviewable = RB.AbstractReviewable.extend({
    defaults: _.defaults({
        caption: '',
        attachmentID: null
    }, RB.AbstractReviewable.prototype.defaults)
});

alert("Model Loaded");
