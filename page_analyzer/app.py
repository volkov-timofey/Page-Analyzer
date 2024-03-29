import os

from flask import Flask, render_template, request, flash, \
    redirect, url_for, make_response
from urllib.parse import urlsplit
from dotenv import load_dotenv

from page_analyzer.utils import is_valid_url, get_urls_, add_url_, \
    get_url_checks, get_pivot_urls_information
from page_analyzer.html_parser import parsing_html


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route("/")
def index(current_url=''):

    if request.args.get('current_url'):
        current_url = request.args.get('current_url')

    return render_template('index.html',
                           current_url=current_url)


@app.post("/urls")
def add_url():

    url = request.form.get('url')

    if not is_valid_url(url):
        flash('Некорректный URL', 'error')

        return make_response(render_template('index.html',
                                             current_url=url), 422)

    normalized_url = f'{urlsplit(url).scheme}://{urlsplit(url).netloc}'

    response = get_urls_(db_url=app.config['DATABASE_URL'],
                         name_table='urls',
                         clause_where=('name', normalized_url))

    if response:
        flash('Страница уже существует', 'info')
        id, name, date_created = next(iter(response))
        return redirect(url_for('get_table_id',
                                id=id,
                                name=name,
                                date_created=date_created,))

    add_url_(db_url=app.config['DATABASE_URL'],
             name_table='urls',
             name_fields=('name', ),
             data_fields=(url, ))

    response = get_urls_(db_url=app.config['DATABASE_URL'],
                         name_table='urls',
                         clause_where=('name', normalized_url))

    id, name, date_created = next(iter(response))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_table_id',
                            id=id,
                            name=name,
                            date_created=date_created,))


@app.get("/urls")
def get_urls():

    response = get_pivot_urls_information(db_url=app.config['DATABASE_URL'])

    return render_template('urls.html', urls=response)


@app.route("/urls/<int:id>")
def get_table_id(id):

    response_url_information = get_urls_(db_url=app.config['DATABASE_URL'],
                                         name_table='urls',
                                         clause_where=('id', id))

    url_information = next(iter(response_url_information))

    response_url_checks = get_url_checks(db_url=app.config['DATABASE_URL'],
                                         name_table='url_checks',
                                         clause_where=('url_id', id))

    return render_template('urls_id.html',
                           url_information=url_information,
                           table_checks=response_url_checks)


@app.post("/urls/<int:id>/checks")
def checks_url(id):
    response = get_urls_(db_url=app.config['DATABASE_URL'],
                         name_table='urls',
                         clause_where=('id', id))

    id, name, _ = next(iter(response))

    tags_information = parsing_html(name)
    if not tags_information:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_table_id', id=id,))

    tags_information['url_id'] = id
    name_fields = tuple(tag for tag in tags_information)
    values_fields = tuple(value for value in tags_information.values())

    add_url_(db_url=app.config['DATABASE_URL'],
             name_table='url_checks',
             name_fields=name_fields,
             data_fields=values_fields)

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_table_id', id=id))
