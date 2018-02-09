from application.application import Application


if __name__ == '__main__':
    app = Application()
    try:
        app.run_spider()
    except KeyboardInterrupt:
        pass
    print(app.spider.render_stats())
    app.stop_spider()