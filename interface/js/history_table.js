function HistoryTable(selector){
    var self = this;

    self.$element = $(selector);
    self.updateDelay = 500;
    self.timerId = null;

}

HistoryTable.prototype.startUpdater = function () {
    var self = this;
    self.timerId = setTimeout(function _timer() {
        self.update();
        self.timerId = setTimeout(_timer, self.updateDelay)
    }, self.updateDelay)
};

HistoryTable.prototype.stopUpdater = function () {
    var self = this;
    self.
};

HistoryTable.prototype.update = function () {
    var self = this;
    spider.get_data(function(d){
        if (d.length){
            self.prependElement(d[0].url);
        }
    });
};

HistoryTable.prototype.prependElement = function (url) {
    var self = this;
    var $newRow = $('<tr style="opacity: 0"><td>'+decodeURI(url)+'</td></tr>');
    self.$element.find('table > tbody').prepend($newRow);
    $newRow.stop().animate({opacity: 1}, 500);
};