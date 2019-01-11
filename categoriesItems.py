# -------------------------------------------------------------
# This is a sample data that was collected from various sites
# Item names and their description were taken from those sites
# -------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Items

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(name='Mohammad Alhashim',
             email='myhony14@gmail.com',
             picture='''https://lh3.googleusercontent.com
             /-G3SKLlQPSbs/AAAAAAAAAAI/AAAAAAAAAZM/j_Cs5kwVQ-k/photo.jpg''',
             provider='google')
session.add(user1)
session.commit()

category1 = Category(name="Soccer", user_id=1)
session.add(category1)
session.commit()

category2 = Category(name="Basketball", user_id=1)
session.add(category2)
session.commit()

category3 = Category(name="Baseball", user_id=1)
session.add(category3)
session.commit()

category4 = Category(name="Frisbee", user_id=1)
session.add(category4)
session.commit()

category5 = Category(name="SnowBoarding", user_id=1)
session.add(category5)
session.commit()

category6 = Category(name="Rock Climbing", user_id=1)
session.add(category6)
session.commit()

category7 = Category(name="Football", user_id=1)
session.add(category7)
session.commit()

category8 = Category(name="Skating", user_id=1)
session.add(category8)
session.commit()

category9 = Category(name="Hockey", user_id=1)
session.add(category9)
session.commit()

item1 = Items(name="Wold Cup 2018 Ball", description='''One of the best
labtops around the world''', category_id=1, user_id=1)
session.add(item1)
session.commit()

item2 = Items(name="Portable Basketball Hoop", description='''This
basketball hoops clear view, shatter proof polycarbonate steel framed backboard
is 50" x 33" and just 1" thick. Speed Shift height adjustment
mechanism lets you raise and lower the hoop with just one hand.
It's the perfect hoop for fun with friends
and family''', category_id=2, user_id=1)
session.add(item2)
session.commit()


item3 = Items(name="Marucci CAT8 BBCOR Bat 2019", description='''One
piece alloy with superior strength, the 2019 Marucci CAT8 BBCOR Bat
provides a higher response rate off the barrel and better durability.
The precision balanced barrel features a ring free multi variable wall
design that creates an expanded sweet spot, while the AV2 Anti-Vibration
knob produces a better feel and less negative vibrational
feedback''', category_id=3, user_id=1)
session.add(item3)
session.commit()

item4 = Items(name="Club Jr Ultimate Gloves", description='''The gloves
consist of an ultra stretch material that will form to your hands on the back
and wrists, and a grippy material to aid in catching and throwing on the
front of the gloves.''', category_id=4, user_id=1)
session.add(item4)
session.commit()

item5 = Items(name="Men's Burton Custom Snowboard", description='''The
mosttrusted board ever, backed by a cult following as snowboardings one
answer to
all terrain''', category_id=5, user_id=1)
session.add(item5)
session.commit()

item6 = Items(name='''La Sportiva Tarantulace Climbing
Shoes''', description='''Designed for the climber looking for a single pair to
do it all, the La Sportiva Tarantulace are jack of all trades climbing shoes
comfortable enough for all day climbs or a trip to the rock
gym.''', category_id=6, user_id=1)
session.add(item6)
session.commit()

item7 = Items(name='''Champro Man-Up TRI FLEX Adult 5 Pad Integrated
Football Girdle''', description='''Featuring TRI FLEX cushioned padding for
the hips, thighs and tailbone. Low-profile and ventilated, these pads
provide the ultimate in protection, flexibility and
comfort.''', category_id=7, user_id=1)
session.add(item7)
session.commit()


item8 = Items(name="SUPER TACKS AS1 STICK", description='''The new
SuperTacks AS1 pushes the boundaries of performance and will
become the new standard for Mid-Kick point sticks. The stiffness
profile has been revisited to maximize loading while providing great
stability and control. Not only can players benefit from a great, powerful
stick, the feel has been substantially improved. The new X Flow technology
allows for a 10g weight reduction while improving compaction for better
durability.''', category_id=9, user_id=1)
session.add(item8)
session.commit()

item9 = Items(name='''adidas Cristiano Ronaldo Juventus
3rd Jersey''', description='''He is Machiavellian in his ruthlessness. Every
teammate of CR7 speaks of his drive to be the best. He takes no prisoners.
He craves to be the greatest footballer ever and he has been finely rewarded
for that mindset. When you wear this 2018/19 adidas Cristiano Ronaldo Juventus
3rd Jersey. You're wearing the shirt of a driven star. You're going to
virtually feel the drive rub off on you even! You're going to give off
vibes of superb ability to all who see you
wear this shirt''', category_id=1, user_id=1)
session.add(item9)
session.commit()

item10 = Items(name='''Nike SuperflyX 6 Elite IC Black Total
Orange''', description='''Its not enough to just be fast, you have to
be the fastest! Its not enough to just be good, you need to be the best!Your
shoe cant just be great, it has to be the greatest! With that being said,
your search for the greatest shoe around should go no further than the Nike
SuperflyX 6 Elite IC! Combining the revolutionary technology Nike has rolled
into the newest Mercurial with a sole designed for optimum performance in the
small sided game, Indoor soccer will
never be the same!''', category_id=1, user_id=1)
session.add(item10)
session.commit()

item11 = Items(name='''Nike Merlin Match Soccer
Ball Hi Vis''', description='''We just need to be noisy and share awesomeness
with you for an unrelenting minute. This 2018/19 Nike Hi Vis Merlin Match
Soccer Ball is such a blast. This may be the most fun ball we've ever had
since we started kicking balls for fun when we were little young guns. We are
scared by how much we love this ball. It is not a controversial statement
around here when we call it the most fun ball. It's also very good in ability.
Everything about this ball screams competence and fun. What a ball it is. It is
a party to own.''', category_id=1, user_id=1)
session.add(item11)
session.commit()

item12 = Items(name='''Nike Ordem V Match Soccer Ball
Premier League   White Crimson''', description='''Aerowtrac grooves allow the
ball to fly accurately towards wherever you send it. This ball is made of
fuse-welded synthetic leather to give you great touch and responsiveness,
as well has make the ball durable, so it can last through all of your games.
The White and Crimson creates a striking look, on the move or on display.
This is the exact ball that the EPL will be using this season, and if you
order today, you can too!''', category_id=1, user_id=1)
session.add(item12)
session.commit()

item13 = Items(name='''Reusch Prisma Supreme G3 Fusion Ortho-Tec
Goalkeeper Gloves   Shocking Orange Blue''', description='''Goalkeepers are
tasked with a very hard job, but with the right tools everything can be made
easier. Goalkeepers look for gloves that provide them with a firm grip on
the ball, support their fingers and look cool while stopping the opposition.
With the Reusch RE:LOAD Suprem G2 Ortho-tec Goalie Gloves all of those
requirements are fulfilled and goalkeepers can be certain that they are
using some of the best gloves out there!''', category_id=1, user_id=1)
session.add(item13)
session.commit()

print("User, Category and an item are added")
