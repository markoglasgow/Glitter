import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'glitter.settings')
import django
django.setup()

import binascii
import random
import re
from datetime import datetime
import calendar
from hashlib import sha1, pbkdf2_hmac
from sys import maxint
from glitter_cms.models import User, Category, Post, Comment, Likes

random.seed(7)

NUM_USERS = 20
NUM_POSTS = 50
NUM_REPLIES = 25
DEFAULT_PASSWORD = 'Glitter123456!'

FIRST_NAMES = ["John", "Robert", "Michael", "William", "James",
               "David", "Richard", "Charles", "Joseph", "Thomas",
               "George", "Kenneth", "Steven", "Edward", "Brian",
               "Charlie"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown",
              "Davis", "Miller", "Wilson", "Moore", "Taylor",
              "Anderson", "Thomas", "Jackson", "White", "Harris",
              "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
              "Lee"]

CATEGORIES = ["Announcements", "Coursework", "Misc"]

TAGS = ["WTS", "WTB", "Selling", "Buying", "Seeking", "Misc", "Party", "Chemistry", "Math", "Textbooks", "Courses"]

SPUN_ARTICLE_TITLES = "{{Looking for|Seeking a|Trying to find} {coursemate|roommate|gaming partner|team member|course help}|{Selling|Willing to sell|WTS|Looking to sell|Want to buy|Buying} {{Math|Chemistry|Computer Science} textbook|gaming console|old car|leftover items|spare booze}|{Party|Even|Get together} at {Maclay|Student residences|Main building|GUU|QMU} this {weekend|Monday|Tuesday|Friday|Saturday|Sunday}}"
SPUN_ARTICLE_BODIES = "{{Hi|Hello|Greetings}, this is a test {post|article|post body|article body} which is {very short|not long|quite short|brief|short|quite brief}. It is also {random|randomly generated|random content|nonsense}. {Hope|It is my hope|We hope} you are not {confused|bedeviled|confuzzled|frazzled}.}"
SPUN_COMMENT_BODIES = "{{Hi|Hello|Greetings}, {I'm interested|this sounds interesting|this looks great}, {how do I contact you|how can I reach you|when are you available|can you have me on FB}?}"

users_list = []
categories_list = []
posts_list = []
comments_list = []


def generate_tags():
    first = TAGS[random.randint(0, len(TAGS) - 1)]
    second = TAGS[random.randint(0, len(TAGS) - 1)]
    third = TAGS[random.randint(0, len(TAGS) - 1)]
    return first + ", " + second + ", " + third


def generate_student_id(last_name):
    char = last_name[0]
    rand_id = random.randint(10000, 99999)
    return "23" + str(rand_id) + char


def generate_timestamp():
    unixtime = calendar.timegm(datetime.utcnow().utctimetuple())
    unixtime = unixtime - 86400
    unixtime = unixtime + random.randint(0, 86400)
    return unixtime


def add_user(name, email, password_hash, salt, student_id):
    user = User.objects.get_or_create(
        name=name,
        email=email,
        password_hash=password_hash,
        salt=salt,
        student_id=student_id,
        recovery_token=''
    )[0]
    user.save()
    return user


def add_category(name):
    category = Category.objects.get_or_create(name=name)[0]
    category.save()
    return category


def add_post(user, category, timestamp, article_title, article_body, tags, likes, views):
    post = Post.objects.get_or_create(
        user=user,
        category=category,
        timestamp=timestamp,
        title=article_title,
        body=article_body,
        tags=tags,
        likes_count=likes,
        view_count=views,
        reply_count=0
    )[0]
    post.save()
    return post


def add_comment(user, post, timestamp, body, likes):
    comment = Comment.objects.get_or_create(
        user=user,
        post=post,
        timestamp=timestamp,
        body=body,
        likes_count=likes
    )[0]
    comment.save()
    return comment


def add_like(user, post=None, comment=None):
    like = Likes.objects.get_or_create(
        user=user
    )[0]
    like.save()
    like = Likes.objects.get(id=like.id)
    like.post = post.id
    like.comment = 0
    like.save()
    return like


def populate_glitter():

    for _ in range(0, NUM_USERS):
        first_name = FIRST_NAMES[random.randint(0, len(FIRST_NAMES) - 1)]
        last_name = LAST_NAMES[random.randint(0, len(LAST_NAMES) - 1)]
        name = first_name + " " + last_name
        student_id = generate_student_id(last_name)
        email = student_id + "@student.gla.ac.uk"
        salt = sha1(str(random.randint(0, maxint))).hexdigest()
        password_hash = binascii.hexlify(pbkdf2_hmac('sha256', DEFAULT_PASSWORD, salt, 10000))

        user = add_user(name, email, password_hash, salt, student_id)
        users_list.append(user)

    for cat_name in CATEGORIES:
        cat_obj = add_category(cat_name)
        categories_list.append(cat_obj)

    for _ in range(0, NUM_POSTS):
        user = users_list[random.randint(0, len(users_list) - 1)]
        category = categories_list[random.randint(0, len(categories_list) - 1)]
        timestamp = generate_timestamp()
        article_title = spin(SPUN_ARTICLE_TITLES)
        article_body = spin(SPUN_ARTICLE_BODIES)
        tags = generate_tags()
        likes = random.randint(0, 5)
        views = random.randint(5, 10)
        post = add_post(user, category, timestamp, article_title, article_body, tags, likes, views)
        posts_list.append(post)

    for _ in range(0, NUM_REPLIES):
        user = users_list[random.randint(0, len(users_list) - 1)]
        post = posts_list[random.randint(0, len(posts_list) - 1)]
        timestamp = generate_timestamp()
        body = spin(SPUN_COMMENT_BODIES)
        likes = random.randint(0, 2)
        comment = add_comment(user, post, timestamp, body, likes)
        comments_list.append(comment)

    # Now add likes to the database to match the like count generated above.
    # for p in posts_list:
    #     if p.likes_count > 0:
    #         likes = p.likes_count
    #         for _ in range(0, likes):
    #             user = users_list[random.randint(0, len(users_list) - 1)]
    #             add_like(user, p)

    # for c in comments_list:
    #     if c.likes_count > 0:
    #         likes = c.likes_count
    #         for _ in range(0, likes):
    #             user = users_list[random.randint(0, len(users_list) - 1)]
    #             add_like(user, None, c)

    return


# Code taken from: https://github.com/AceLewis/spintax/blob/master/spintax/spintax.py
def _replace_string(match):
    """
    Function to replace the spintax with a randomly chosen string
    :param match object:
    :return string:
    """
    global spintax_seperator, random_string
    test_string = re.sub(spintax_seperator, lambda x: x.group(1)+random_string, match.group(2))
    random_picked = random.choice(re.split(random_string, test_string))
    return match.group(1) + random_picked + match.group(3)


# Code taken from: https://github.com/AceLewis/spintax/blob/master/spintax/spintax.py
def spin(string, seed=None):
    """
    Function used to spin the spintax string
    :param string:
    :param seed:
    :return string:
    """

    # As look behinds have to be a fixed width I need to do a "hack" where
    # a temporary string is used. This string is randomly chosen. There are
    # 1.9e62 possibilities for the random string and it uses uncommon Unicode
    # characters, that is more possibilerties than number of Planck times that
    # have passed in the universe so it is safe to do.
    global random_string
    random_string = "57igrhdg758grjkgber7i5ghkjer45"

    # If the user has chosen a seed for the random numbers use it
    if seed is not None:
        random.seed(seed)

    # Regex to find spintax seperator, defined here so it is not re-defined
    # on every call to _replace_string function
    global spintax_seperator
    spintax_seperator = r'((?:(?<!\\)(?:\\\\)*))(\|)'
    spintax_seperator = re.compile(spintax_seperator)

    # Regex to find all non escaped spintax brackets
    spintax_bracket = r'(?<!\\)((?:\\{2})*)\{([^}{}]+)(?<!\\)((?:\\{2})*)\}'
    spintax_bracket = re.compile(spintax_bracket)

    # Need to iteratively apply the spinning because of nested spintax
    while True:
        new_string = re.sub(spintax_bracket, _replace_string, string)
        if new_string == string:
            break
        string = new_string

    # Replaces the literal |, {,and }.
    string = re.sub(r'\\([{}|])', r'\1', string)
    # Removes double \'s
    string = re.sub(r'\\{2}', r'\\', string)

    return string



def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/"} ]
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/"} ]
    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"} ]
    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16} }
    # If you want to add more catergories or pages,
    # add them to the dictionaries above.
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
                add_page(c, p["title"], p["url"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=17):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting Glitter population script...")
    populate_glitter()
