import os
from collections import defaultdict

import click
from flask import current_app, g
from flask.cli import with_appcontext
from hobbyProjectWebsite import create_app
from werkzeug.security import check_password_hash, generate_password_hash

