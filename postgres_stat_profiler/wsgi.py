from postgres_stat_profiler import create_app

if __name__ == "__main__":
    app = create_app()
    app.debug = False
    app.run(ssl_context='adhoc')