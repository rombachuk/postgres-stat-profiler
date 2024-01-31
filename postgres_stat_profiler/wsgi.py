from postgres_stat_profiler import create_app

def main():
    app = create_app()
    app.debug = False
    app.run(ssl_context='adhoc')

if __name__ == "__main__":
   main()