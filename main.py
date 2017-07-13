from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "some_secret"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:teddybear@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(max))
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog')
def index():

    #must use this line in this project basically
    #makes a mulidictionary with the parsed contents of the query String
    #passing the key id in to th
    #
    if request.args.get('id'):
        post_id = request.args.get('id')
        #render individual blog post page, with list of posts
        posts = Blog.query.filter_by(id=post_id)
        return render_template("post.html", posts=posts)
    else:
        #grab all posts in the database
        posts = Blog.query.all()
        #render main blog page
        return render_template('blog.html',
                                title="Post Things!",
                                posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':

        post_title = request.form['post-title']
        post_body = request.form['text-area']

        if not is_title_empty() and not is_body_empty():

            post = Blog(post_title, post_body)
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            return redirect('/blog?id={}'.format(post_id))
        else:
            if is_title_empty():
                flash("Please provide a title for your post")
            if is_body_empty():
                flash("Please provide some content for your post")
            return render_template("newpost.html",
                                    title="Try Again!",
                                    post_title=post_title,
                                    post_body=post_body)

    return render_template("newpost.html",
                            title="New Post!")

def is_title_empty():
    post_title = request.form['post-title']
    if post_title != "":
        return False
    return True

def is_body_empty():
    post_body = request.form['text-area']
    if post_body != "":
        return False
    return True

if __name__ == '__main__':
    app.run()
