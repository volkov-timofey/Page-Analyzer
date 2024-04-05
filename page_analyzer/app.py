import os

from flask import Flask, render_template, request, flash, \
    redirect, url_for
from urllib.parse import urlsplit
from dotenv import load_dotenv

from page_analyzer.database import DataBase
from page_analyzer.html_parser import parse_html
from page_analyzer.utils import is_valid_url


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route("/")
def index(current_url=''):

    if request.args.get('current_url'):
        current_url = request.args.get('current_url')

    return render_template('index.html', current_url=current_url)


@app.post("/urls")
def add_url():

    url = request.form.get('url')

    if not is_valid_url(url):
        flash('Некорректный URL', 'error')

        return render_template('index.html', current_url=url), 422

    normalized_url = f'{urlsplit(url).scheme}://{urlsplit(url).netloc}'

    db = DataBase(app.config['DATABASE_URL'])
    urls = db.get_urls(normalized_url)

    if urls:
        flash('Страница уже существует', 'info')
        id, name, date_created = next(iter(urls))
        return redirect(url_for('get_table_id',
                                id=id,
                                name=name,
                                date_created=date_created,))

    db.add_url(normalized_url)

    urls = db.get_urls(normalized_url)

    db.close_connect_db()

    id, name, date_created = next(iter(urls))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_table_id',
                            id=id,
                            name=name,
                            date_created=date_created,))


@app.get("/urls")
def get_urls():

    db = DataBase(app.config['DATABASE_URL'])
    urls = db.get_urls_with_checks()
    db.close_connect_db()

    return render_template('urls.html', urls=urls)


@app.route("/urls/<int:id>")
def get_table_id(id):

    db = DataBase(app.config['DATABASE_URL'])

    url = db.get_urls_by_id(id)
    url = next(iter(url))

    url_checks = db.get_url_checks(id)

    db.close_connect_db()

    return render_template('urls_id.html',
                           url_information=url,
                           table_checks=url_checks)


@app.post("/urls/<int:id>/checks")
def checks_url(id):

    db = DataBase(app.config['DATABASE_URL'])

    urls = db.get_urls_by_id(id)
    id, name, _ = next(iter(urls))
    tags_information = parse_html(name)

    if not tags_information:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_table_id', id=id,))

    tags_information['url_id'] = id

    db.add_url_checks(tags_information)

    db.close_connect_db()

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_table_id', id=id))
