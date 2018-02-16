/**
 * @param {Spider} spider
 * @constructor
 */
function SpiderMonitor(spider){
    var self = this;

    self.spider = spider;
    self.updateTime = 100;
    self.timerId = null;
    self.isUpdating = {};
    self.forceUpdate = false;
}

SpiderMonitor.prototype.start = function () {
    var self = this;
    if (self.timerId === null){
        self.timerId = setTimeout(function _timer() {
            self.update();
            self.timerId = setTimeout(_timer, self.updateTime)
        }, self.updateTime);
    }
};

SpiderMonitor.prototype.stop = function () {
    var self = this;
    if (self.timerId !== null){
        clearTimeout(self.timerId);
        self.timerId = null;
    }
};

SpiderMonitor.prototype.update = function(){
    var self = this;
    if (self.canUpdate('data')){
        self.isUpdating.data = true;
        self.spider.controller.get_data(function(d){
            self.isUpdating.data = false;
            if (d.length){
                self.spider.addVisitedLink(d[0]);
            }
        });
    }
    if (self.canUpdate('state')){
        self.isUpdating.state = true;
        self.spider.controller.get_state(function(s){
            self.isUpdating.state = false;
            self.spider.setState(s);
        });
    }
};

/**
 * @param {string} what
 * @returns {boolean}
 */
SpiderMonitor.prototype.canUpdate = function(what){
    var self = this;
    return !(what in self.isUpdating) || !self.isUpdating[what] || self.forceUpdate;
};