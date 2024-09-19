from app import create_app, init_db
import click

app = create_app()
init_db(app)

@click.command()
@click.option('--debug', is_flag=True, help='Run the app in debug mode')
@click.option('--host', default='127.0.0.1', help='The interface to bind to')
@click.option('--port', default=5000, help='The port to bind to')
def run(debug, host, port):
    """Run the Flask application."""
    click.echo(f'Starting AI Tutor on {host}:{port}')
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    run()