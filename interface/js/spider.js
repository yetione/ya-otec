/**
 * @param spiderObject
 * @constructor
 */
function Spider(spiderObject){
    var self = this;
    self.controller = spiderObject;
    self.visitedLinks = [];
    self.state = null;

    self.monitor = new SpiderMonitor(self);
    self.monitor.start();
}

Spider.prototype.start = function (callback) {
    var self = this;
    self.controller.start(function(state){
        self.setState(state);
        if (callback){
            callback(state);
        }
    });
};

Spider.prototype.stop = function (callback) {
    var self = this;
    self.controller.stop(function(state){
        self.setState(state);
        if (callback){
            callback(state);
        }
    });
};

/**
 * @param {boolean} state
 */
Spider.prototype.setState = function (state) {
    var self = this;
    if (self.state !== state){
        self.state = state;
        $(document).trigger('spiderStateChange', state, self);
    }
};

/**
 * @param {object} link
 */
Spider.prototype.addVisitedLink = function(link){
    var self = this;
    self.visitedLinks.push(link);
    $(document).trigger('spiderVisitedLinkAdd', link, self);
};

/**
 * @param {string} url
 */
Spider.prototype.prependElement = function (url) {
    var self = this;
    var $newRow = $('<tr style="opacity: 0"><td>'+decodeURI(url)+'</td></tr>');
    self.$element.find('tbody').prepend($newRow);
    $newRow.stop().animate({opacity: 1}, 500);
};

Spider.prototype.clear = function(){
    var self = this;
    self.$element.find('tbody').html('');
};