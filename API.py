import sqlite3
from flask import Flask, request, Response, render_template
from jinja2 import Environment, PackageLoader
from markupsafe import escape
from flask import make_response
from flask import session
from flask import Flask,redirect

app = Flask(__name__)
auth_manager = AuthManager()