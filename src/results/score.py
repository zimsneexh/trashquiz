class score():

    scores = { }
    
    @staticmethod
    def add_score(user, num_correct):
        score.scores[user] = num_correct

    @staticmethod
    def get_scores():
        return score.scores
