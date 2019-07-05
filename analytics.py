from collections import Counter
import pandas as pd
from copy import copy
import spacy
from utils import Names
from person import Person
import operator
import nlp_support as nlps


class Analyzer:

    DAY_OF_WEEK = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    WORDS_TO_EXCLUDE = {'http', 'https', 'co', 'rt', 'realdonaldtrump', 'trump', 'u', 'many'}

    def __init__(self, path: str, user_name='', user_id=None):
        self.user_name = user_name
        self.user_id = user_id
        self.statuses = pd.read_csv(path)
        self.statuses['date'] = self.statuses['date'].apply(nlps.str_to_date)
        self.name_dict = Names().name_dict

    def words_counter_old(self):
        """
        Given the path to a csv file of the retrieved statuses, Return sorted word counter
        :return: dict
        """
        word_counter = Counter()
        statuses = self.statuses
        for status_content in statuses['content']:

            tokens = nlps.parse_text(status_content)

            # Put in counter
            for w in tokens:
                word_counter[w] += 1

        return word_counter

    def words_counter(self, special_counter=None):
        """
        Given the path to a csv file of the retrieved statuses, Return sorted word counter
        :param special_counter: None, place or person
        :return: dict
        """
        word_counter = Counter()
        statuses = self.statuses
        nlp = spacy.load('en_core_web_sm')
        for status_content in statuses['content']:

            # Pre-processing the text
            status_content = nlps.remove_punctuation(status_content)
            status_content = nlps.remove_stopwords_from_str(status_content)

            doc = nlp(u"{}".format(status_content))
            if special_counter is None:
                for token in doc:
                    word_counter[token.lemma_] += 1
            elif special_counter == 'place':
                for ent in doc.ents:
                    if ent.label_ == 'GPE':
                        word_counter[ent.text.lower()] += 1
        word_counter = sorted(word_counter.items(), key=operator.itemgetter(1), reverse=True)
        return word_counter

    def person_counter(self):
        """
        Identify persons names, and count them. Overcome nicknames (Robert Mueller VS Bob Mueller), and assign single
        word names ('Hillary said that...') to the most likely person
        :return: counter
        """
        person_counter = Counter()
        statuses = self.statuses
        nlp = spacy.load('en_core_web_sm')
        single_word_name_persons = []
        for status_content in statuses['content']:
            # Pre-processing the text
            status_content = nlps.remove_punctuation(status_content)
            status_content = nlps.remove_stopwords_from_str(status_content)
            status_content = nlps.remove_belonging(status_content)
            # Creating the spacy doc
            doc = nlp(u"{}".format(status_content))
            for ent in doc.ents:
                if not ent.label_ == 'PERSON':
                    continue
                person = Person()
                person.assign_name(ent.lower_, self.name_dict)
                if person.last is None:
                    single_word_name_persons.append(person)
                    continue
                for existing_person in person_counter.keys():
                    if existing_person.is_the_same_person(person):
                        person_counter[existing_person] += 1
                        person = None
                        break
                if person is not None:  # No person was found equal to him in counter
                    person_counter[person] = 1
                    # If a name has only one word, find full name

        # Dealing with a single name (e.g. 'Hillary') person we found. Assign it to the most frequent person with the
        # same first name, if exists
        for single_word_person in single_word_name_persons:
            full_person = single_word_person.get_full_name(person_counter)
            person_counter[full_person] += 1
        person_counter_beautify = {str(k): v for k, v in person_counter.items()}
        person_counter_beautify = sorted(person_counter_beautify.items(), key=operator.itemgetter(1), reverse=True)
        return person_counter_beautify

    def get_statuses_by_words(self, words: list):
        """
        Given a list of words, return all the statuses that contain these words
        :param words:
        :return: data frame text and date
        """
        res = []
        for index, status in self.statuses.iterrows():
            tokens_set = set(nlps.parse_text(status['content']))  # We get free duplicates collection, and O(1) search
            contain = True
            for word in words:
                if word not in tokens_set:
                    contain = False
                    break
            if contain:
                res.append([status['date'], status['content']])
        return pd.DataFrame(data=res, columns=['date', 'content'])

    def get_most_active_hour(self):
        """
        Returns the hour of the day the user tweets the most
        :return: The hour (int) with the highest number of tweets
        """
        # Copying and adding a new column called hour derived from the date column
        my_statuses = copy(self.statuses)
        my_statuses['hour'] = [date.hour for date in my_statuses['date']]
        # Grouping by hour and returning the label (which is hour) with the highest value (count)
        my_statuses_gb = my_statuses.groupby('hour').count()['date']
        return my_statuses_gb.idxmax()

    def number_of_tweets_by_dow(self):
        """
        Group by day of week and count the number of tweets
        """
        # Copying and adding a new column called hour derived from the date column
        my_statuses = copy(self.statuses)
        my_statuses['dow'] = [self.DAY_OF_WEEK[date.weekday()] for date in my_statuses['date']]
        # Grouping by hour and returning the label (which is hour) with the highest value (count)
        my_statuses_gb = my_statuses.groupby('dow').count()['date']
        return my_statuses_gb.idxmax()  # change to all days

