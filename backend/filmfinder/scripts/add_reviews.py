from login.models import User
from movies.models import Movie, Review
import numpy as np
import random
import time
import datetime


def run():

    def str_time_prop(start, end, format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))

    def random_date(start, end, prop):
        return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

    pos_reviews = [
       "This is movie is unusual, but it works for me. It kept me intrigued from the beginning with the plot which is not entirely clearly, but that made it more interesting for me. There's a lot of action in the movie which I found excellent and enjoyed a lot. It might not be realistic, but its a movie so it doesn't have to be. The plot is amazing and I can't wait to watch volume 2 soon because of how intriguing volume 1 was.",
        '''Man, what a film. As a fan of 70's martial arts movies, it was great to see all of the references. I also thought the use of B&W throughout was extremely effective. The cartoon sequences seemed a bit much, but did fit in with the overall feel of the film. I have seen many people posting about the sheer amount of blood and guts, but you have to remember this was Tarantino's homage to Bruce Lee-era action pictures. In those movies, the stories were very similar epics of revenge, and they never had much of a budget for good "gore" effects. It was more or less "throw some fake blood on the guy who just got killed" type of effects, which were duplicated accurately by some of the deaths in this movie. The plot also followed closely the plot of most 70's Kung Fu movies; something despicable happens to the weak hero (whole village razed, family slaughtered, etc..)''',
    ]
    neg_reviews = [
        "The biggest overrated nonsense since the Blair Witch Project. If you like cheap Chinese b-movies, then I guess you'll love this load of garbage. It was ok for about the first 20 minutes, then it becomes untolerable.",
        "This has got to be the worst movie that I have seen. The story is jumbled with short segments of movie broken by carton segments. There is nothing to make this movie worth seeing, in fact it was bad enough that the entire group voted to leave after 50 minutes. The scene transitions are so poorly done I thought it could be done better as a school project.",
        """I cannot fathom two things: how this movie cost so much to produce, and why they wasted so much money doing so. This movie like watching a documentary about a political campaign that never ends. Seriously, save yourself 3 hours of the most boring and monotonous mash up ever. There is virtually no action or incentive to keep watching. It's 90% people talking at tables with lines like "Who said that?! oh he said that?!" or "Ok, well you talk to him Frank!" and then Frank talks to him, and then Frank talks to the other guys, and then Frank talks to him, and rinse and repeat. Occasionally a few seconds are spared for shooting someone in the head and then that's it. You are constantly left searching for a reason to keep watching, but it never comes."""
    ]

    neutral_reviews = [
        "I don't know where to start on this one other than thanking Netflix for being the only distributor to fund this movie so we could see Big screen legends take their last big swing. The set and screen is smaller than I liked it to be, it being released on a streaming site but it's better than never seeing it. It's not a flawless movie and I wouldn't necessarily call it a masterpiece or something new and innovative. But for an old genre gangsta flick it's easily one of the best ones out there.",
        " If your one of those people thinking about getting Netflix just so you can see this dinosaur, please don't. Watching Robert DeNero in this film is almost sad. He plays the part of a guy in his prime, but the CGI face doesn't work. It looks animated at times and his body moves like a very old man ... even for DeNero's age of mid 70's. The grocery sceen where DeNero beats up the store owner is just embarrassing to watch. Joe Pesci comes out of retirement for this one and shines. He has a stare that burns a hole through you. Al Pacino as the flamboyant Jimmy Hoffa works well. Harvey's Keitel in a small mob boss roll is solid too. But the editing is not together ... the movis drags ... and the fellas in the film unfortunately are just too old to pull this off convincingly. It's too bad this wasn't made 25 years ago, it would have probably worked. Grossly overhyped epic that is passed its prime, in more than one way. Would never waste 3.5 hrs watching again. If your hoping for the next Goodfellas, you've come to the wrong place."
    ]

    # user_id [1, 23]
    # movie_id [4, 215]

    for mid in range(4, 216):
        uid = set(np.random.randint(low=1, high=23, size=12))
        movie_obj = Movie.objects.get(mid=mid)
        date = random_date(str(Movie.objects.get(mid=mid).released_date)[:-6], str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), random.random())
        for user in uid:
            rating = round(np.random.uniform(low=0, high=5, size=1)[0], 1)
            user_obj = User.objects.get(uid=user)
            try:
                if rating <= 2:
                    Review.objects.create(review_comment=neg_reviews[np.random.randint(low=0, high=2)],
                                          rating_number=rating, user=user_obj, movie=movie_obj, date=date)
                elif rating >= 4:
                    Review.objects.create(review_comment=pos_reviews[np.random.randint(low=0, high=1)],
                                          rating_number=rating, user=user_obj, movie=movie_obj, date=date)
                else:
                    Review.objects.create(review_comment=neutral_reviews[np.random.randint(low=0, high=2)],
                                          rating_number=rating, user=user_obj, movie=movie_obj, date=date)
            except:
                continue

    print('DONE')
