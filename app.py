from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail, Message
from threading import Thread
from functools import wraps
from forms import ContactForm
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = config.SENDER_EMAIL
app.config["MAIL_PASSWORD"] = config.SENDER_PASS
app.config["MAIL_DEFAULT_SENDER"] = config.SENDER_EMAIL
mail = Mail(app)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async
def send_async_email(flask_app, msg):
    with flask_app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, text_body, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


@app.route('/', methods=('GET', 'POST'))
def index():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            send_mail(
                "New message from portfolio",
                recipients=[config.RECEIVER],
                text_body="Email: {} \n"
                          "Message: {}".format(form.email.data, form.message.data)
            )
            return redirect(url_for('index'))
        else:
            return render_template('index.html', form=form, scroll='contact')
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
