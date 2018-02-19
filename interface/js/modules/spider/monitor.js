import $ from  "jquery";

export default class SpiderMonitor {
    /**
     * @param {Spider} spider
     */
    constructor(spider) {
        this.spider = spider;
        this.updateTime = 100;
        this.timerId = null;
        this.isUpdating = {};
        this.forceUpdate = false;
    }

    start() {
        let self = this;
        if (self.timerId === null){
            self.timerId = setTimeout(function _timer() {
                self.update();
                self.timerId = setTimeout(_timer, self.updateTime)
            }, self.updateTime);
        }
    }

    stop() {
        let self = this;
        if (self.timerId !== null){
            clearTimeout(self.timerId);
            self.timerId = null;
        }
    }

    update() {
        let self = this;
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
    }

    canUpdate(what) {
        return !(what in this.isUpdating) || !this.isUpdating[what] || this.forceUpdate;
    }
}