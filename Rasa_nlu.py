from rasa_nlu.rasa_nlu.training_data import load_data
from rasa_nlu.rasa_nlu.model import Trainer
from rasa_nlu.rasa_nlu.model import Interpreter
from rasa_nlu.rasa_nlu.config import load
from Bot import Bot


class Rasa_NLU(object):

    def __init__(self):
        self.data_training = "testData.json"
        self.Bot = Bot()
        self.training_nlu()

    def training_nlu(self):
        training_data = load_data(self.data_training)
        config = load("config_spacy.yml")
        trainer = Trainer(config)
        trainer.train(training_data)
        model_directory = trainer.persist("projects")
        self.interpreter = Interpreter.load(model_directory)


    def parse_message(self, message):
        parsed_message = self.interpreter.parse(message)
        return parsed_message

    def check_entities(self, dic):
        for k,v in dic.items():
            if k == 'genres':
               result =  self.Bot.choose_film_by_genres(v)
               return result


    def find_respond_from_bot(self, message):
        parse_mes = self.parse_message(message)
        #print(parse_mes)
        if parse_mes['intent']['name'] == 'greet':
            result = self.Bot.hello_message()
            return result

        if parse_mes['intent']['name'] == 'popular_film':
            result = self.Bot.popular_film()
            return result

        if parse_mes['intent']['name'] == 'goodbye':
            result = self.Bot.goodbye_message()
            return result

        if parse_mes['intent']['name'] == 'affirm':
            result = self.Bot.aff_message()
            return result
        if parse_mes['intent']['name'] == 'new_search':
            result = self.Bot.new_search()
            return result

        if parse_mes['intent']['name'] == 'thanks':
            result = self.Bot.thanks_message()
            return result

        if parse_mes['intent']['name'] == 'film_search':
            params = {}
            if len(parse_mes['entities']) > 0:
                for e in parse_mes['entities']:
                    params[e["entity"]] = str(e['value'])
                result = self.check_entities(params)
                return result

        if not "intent" in parse_mes or parse_mes['intent'] is None:
            result = self.Bot.bad_message()
            return result

        return self.Bot.bad_message()


