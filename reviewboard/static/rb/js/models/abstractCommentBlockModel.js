/*
 * Represents a region of reviewable content that contains comments.
 *
 * This stores all comments that match a given region, as defined by a
 * subclass of AbstractCommentBlock.
 *
 * New draft comments can be created, which will later be stored on the
 * server.
 *
 * The total number of comments in the block (including any draft comment)
 * will be stored, which may be useful for display.
 */
RB.AbstractCommentBlock = Backbone.Model.extend({
    defaults: {
        hasDraft: false,
        canDelete: false,
        draftComment: null,
        serializedComments: [],
        count: 0
    },

    /*
     * Initializes the AbstractCommentBlock.
     */
    initialize: function() {
        var comments = this.get('serializedComments'),
            newSerializedComments = [];

        /*
         * Find out if there's any draft comments, and filter them out of the
         * stored list of comments.
         */
        if (comments.length > 0) {
            _.each(comments, function(comment) {
                // We load in encoded text, so decode it.
                comment.text = $("<div/>").html(comment.text).text();

                if (comment.localdraft) {
                    this.ensureDraftComment(comment.comment_id, comment.text);
                } else {
                    newSerializedComments.push(comment);
                }
            }, this);

            this.set('serializedComments', newSerializedComments);
        } else {
            this.ensureDraftComment();
        }

        this.on('change:draftComment', this._updateCount, this);
        this._updateCount();
    },

    /*
     * Returns whether or not the comment block is empty.
     *
     * A comment block is empty if there are no stored comments and no
     * draft comment.
     */
    isEmpty: function() {
        return this.get('serializedComments').length === 0 &&
               !this.has('draftComment');
    },

    /*
     * Creates a draft comment, optionally with a given ID and text.
     *
     * This must be implemented by a subclass to return a Comment class
     * specific to the subclass.
     */
    createComment: function(id) {
        console.assert(false, 'This must be implemented by a subclass');
    },

    /*
     * Creates a draft comment in this comment block.
     *
     * Only one draft comment can exist per block, so if one already exists,
     * this will do nothing.
     *
     * The actual comment object is up to the subclass to create.
     */
    ensureDraftComment: function(id, text) {
        var self = this,
            comment;

        if (this.has('draftComment')) {
            return;
        }

        comment = this.createComment(id);

        if (text) {
            comment.text = text;
        }

        $.event.add(comment, 'destroyed', function() {
            self.set('draftComment', null);
            self._updateCount();
        });

        $.event.add(comment, 'saved', _.bind(this._updateCount, this));

        this.set('draftComment', comment);
    },

    /*
     * Updates the displayed number of comments in the comment block.
     *
     * If there's a draft comment, it will be added to the count. Otherwise,
     * this depends solely on the number of published comments.
     */
    _updateCount: function() {
        var count = this.get('serializedComments').length;

        if (this.has('draftComment')) {
            count++;
        }

        this.set('count', count);
    }
});
