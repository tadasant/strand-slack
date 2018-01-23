import os

from src import create_app


def create_logs_dir_if_not_exists():
    if not os.path.exists('logs'):
        os.mkdir('logs')


if __name__ == '__main__':
    create_logs_dir_if_not_exists()
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
