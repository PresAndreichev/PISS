def is_valid_score(score):
    return 1 <= score <= 10


class Review:
    def __init__(self, user_reviewer, score, object_which_is_reviewed, publish_anonymous=False, text=""):
        self.__user = user_reviewer  # this is an user object
        self.__score = Review.__DEFAULT_SCORE
        if is_valid_score(score):
            self.__score = score
        self.__object_which_is_reviewed = object_which_is_reviewed  # this is a object (subject, event)
        self.__publish_anonymous = publish_anonymous
        self.__text = text

    __DEFAULT_SCORE = 5

    def __init__(self, review_id):
        self.__user, self.__score, self.__object_which_is_reviewed, self.__publish_anonymous, self.__text =
        load_review_from_id(review_id)

    """ __init__(self, scores):
        self.__scores = []
        if type(scores) is int:
            if is_valid_score(scores):
                self.__scores.append(scores)
        else:
            self.__scores = list(filter(is_valid_score, scores))  # filter out invalid scores
        self.__count = len(self.__scores)
        self.__average_rating = 0  # 0 means not set yet, otherwise out of scale from 1 to 10
        if self.__count != 0:
            self.__average_rating = sum(self.__scores) / self.__count

    def add_score(self, score):
        if is_valid_score(score):
            self.__average_rating = self.__count * self.__average_rating + score
            self.__round_average_rating()
            self.__scores.append(score)
            self.__count += 1
            self.__average_rating /= self.__count

    def get_scores(self):
        return self.__scores

    def get_count(self):
        return self.__count

    def get_average_rating(self):
        return self.__average_rating

    def __round_average_rating(self):
        whole_part = int(self.__average_rating)
        double_part = self.__average_rating - whole_part
        self.__average_rating = int(self.__average_rating)
        if double_part >= 0.5:
            self.__average_rating += 1"""