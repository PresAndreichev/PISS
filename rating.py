class Rating:
    def __is_valid_score(self, score):
        return 1 <= score <= 10

    def __round_average_rating(self):
        whole_part = int(self.__average_rating)
        double_part = self.__average_rating - whole_part
        self.__average_rating = int(self.__average_rating)
        if double_part >= 0.5:
            self.__average_rating += 1

    def __init__(self, scores):
        self.__scores = []
        if type(scores) is int:
            if self.__is_valid_score(scores):
                self.__scores.append(scores)
        else:
            self.__scores = list(filter(self.__is_valid_score, scores))  # filter out invalid scores
        self.__count = len(self.__scores)
        self.__average_rating = 1  # Of scale from 1 to 10
        if self.__count != 0:
            self.__average_rating = sum(self.__scores) / self.__count

    def add_score(self, score):
        if self.__is_valid_score(score):
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
