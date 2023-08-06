from .abstract import *

class ScoreList():
    def __init__(self, assessment_id, doc_count):
        self.assessment_id = assessment_id
        self.doc_count = doc_count
        self.scores = []

    def append(self, score):
        self.scores.append(score)


class ScoreItem():
    def __init__(self, date, score, doc_count):
        self.date = date
        self.score = score
        self.doc_count = doc_count


class Score( ListableAPIResource ):
    @classmethod
    def by_date(cls, interval, assessment_id = None):
        """
        Lists assessment run scores by date.

        Args:
            interval (mage.schema.DateInterval):
            assessment_id (str, optional):

        Returns:
            List of `ScoreList`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Score.by_date('YEAR')
        """

        from mage import client_id

        retval = []
        result = cls._retrieve_all('scores_by_date', client_id=client_id, interval=interval)
        for assessment in result:
            score_list = ScoreList(assessment.data['key'], assessment.data['doc_count'])
            for interval in assessment.data['scores_by_interval']['buckets']:
                score = ScoreItem(interval['scores'], interval['key_as_string'], interval['doc_count'])
                score_list.append(score)

            if assessment.data['key'] == assessment_id:
                return  score_list

            retval.append(score_list)

        return retval
