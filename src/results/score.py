class score():

    scores = { }

    def add_score(self, user, num_correct):
        score.scores[user] = num_correct

    def get_scores(self):
        return score.scores
