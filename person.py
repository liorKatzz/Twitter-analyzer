

class Person:

    WORDS_TO_EXCLUDE = {'crooked', 'china', 'sleepy', 'repo', 'report', 'repor', 'japan'}   # Words that spacy got wrong

    def __init__(self):
        self.first = None
        self.last = None
        self.first_synonyms = []

    def assign_name(self, full_name: str, name_dict):
        tokens = full_name.split()
        # Filter words that I don't want:
        tokens = [token for token in tokens if token not in self.WORDS_TO_EXCLUDE]
        self.first = tokens[0]
        try:
            self.first_synonyms = name_dict[self.first]
        except KeyError:
            pass
        if len(tokens) > 1:
            self.last = tokens[-1]

    def is_the_same_person(self, person):
        """
        Given another person, check if their first synonyms are the same by checking if the first name of each is in the
        other's synonyms
        :param person:
        :return: True/False
        """
        return ((self.first in person.first_synonyms and person.first in self.first_synonyms) or self.first ==
                person.first) and self.last == person.last

    def is_the_same_person_by_single_name(self, single_person):
        return (self.first in single_person.first_synonyms and single_person.first in self.first_synonyms) or \
               single_person.first == self.first or single_person.first == self.last

    def is_contain_name(self, name):
        if self.first == name or self.last == name:
            return True
        return False

    def get_full_name(self, counter):
        """Given a person with a single word name, find a person with the same first name. If there is more than one,
        return the person with most frequencies
        """
        res_person = None
        max_ = -1
        for existing_person in counter.keys():
            if existing_person.is_the_same_person_by_single_name(self) and counter[existing_person] > max_:
                res_person = existing_person
                max_ = counter[existing_person]
        if res_person is not None:
            return res_person
        return self

    def __str__(self):
        if self.last:
            return self.first + ' ' + self.last
        return self.first

