from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login
from app import db
from hashlib import md5
from time import time
import jwt
from app import app

#Define the association table
followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

#Unit testing for the entire User Model is found in microblog/tests.py
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_see = db.Column(db.DateTime, default=datetime.utcnow)

    #Each call here will first define user as the parent class in relation to the followers defined above
    #Link to database diagram: https://blog.miguelgrinberg.com/static/images/mega-tutorial/ch08-followers-schema.png
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        #set_password uses Flasks password hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        #Verify the password, existing hashed against password input
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        #Gravatar is used for randomized hexagonal profile pics
        #TODO: Allow for user to add their own profile pic at profile creation and in edit.
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    def get_reset_password_token(self, expires_in=600):
        #Create a JSON Webtoken for password reset, expires in 10 minutes
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
                app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                algorithms=["HS256"])['reset_password']
        except:
            return
        return User.query.get(id)
        

    #For more reusability these methods are implemented to handle adding, and removing, followers.
    #START
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    #END

    def followed_posts(self):
        '''
        This function will use a database query to avoid sorting posts for user with
        a large amount of user followed.

        It does so by first joining all posts found in the left side of the join,
        and append any record from the followers, right side of the join that match
        user.id condition. This can cause duplication.

        The query made on the Post class is then filtered to only return a table with
        posts where the follower id is equal to the id of the User in question, 
        meaning that only posts where the author has the specific user as a follower
        will be returned.

        After that the posts are simply sorted by their timestamp in the database.

        The initial query does not allow the User's own posts to be added so it a seperate
        query adds them, and then merges them with the exisitng table, and sorts all the
        posts again.
        '''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))