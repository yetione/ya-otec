import SpiderMonitor from "./monitor";
import $ from  "jquery";

export default class Spider{
    /**
     * @param spiderObject
     */
    constructor(spiderObject) {
        this.controller = spiderObject;
        this.visitedLinks = [];
        this.state = null;
        this.monitor = new SpiderMonitor(this);
        this.monitor.start();
    }

    start(callback) {
        let self = this;
        self.controller.start(function (state) {
            self.setState(state);
            if (callback){
                callback(state);
            }
        });
    }

    stop(callback) {
        let self = this;
        self.controller.stop(function (state) {
            self.setState(state);
            if (callback){
                callback(state);
            }
        });
    }

    setState(state) {
        if (this.state !== state){
            this.state = state;
            $(document).trigger('spiderStateChange', state, this);
        }
    }

    addVisitedLink(link) {
        this.visitedLinks.push(link);
        $(document).trigger('spiderVisitedLinkAdd', link, this);
    }
}