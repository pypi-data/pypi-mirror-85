import aiohttp, aiodns, asyncio, json
from random import shuffle
from base64 import b64decode



class InvalidParameters(Exception):
    
    '''Raised when invalid parameters are passed'''

    pass



class TriviaWrapper():
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.token = loop.run_until_complete(self.request('https://opentdb.com/api_token.php?command=request'))['token']
        self.questions = []
        self.categories = [
            'General Knowledge',
            'Entertainment: Books',
            'Entertainment: Film',
            'Entertainment: Music',
            'Entertainment: Musicals & Theatres',
            'Entertainment: Television',
            'Entertainment: Video Games',
            'Entertainment: Board Games',
            'Science & Nature',
            'Science: Computers',
            'Science: Mathematics',
            'Mythology',
            'Sports',
            'Geography',
            'History',
            'Politics',
            'Art',
            'Celebrities',
            'Animals',
            'Vehicles',
            'Entertainment: Comics',
            'Science: Gadgets',
            'Entertainment: Japanese Anime & Manga',
            'Entertainment: Cartoon & Animations',
        ]
        self.difficulties = [
            'easy',
            'medium',
            'hard'
        ]
        self.types = [
            'multiple',
            'boolean'
        ]
    

    async def request(self, query):
        conn = aiohttp.TCPConnector(resolver=aiohttp.AsyncResolver())
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(query) as response:
                r = await response.json()
                if r['response_code'] == 3:
                    self.token = (await self.request('https://opentdb.com/api_token.php?command=request'))['token']

                return r


    def cacheRequest(self, amount=10, category=None, difficulty=None, quizType=None):
        stringCategory = self.categories[category-9] if category else ''

        return [question for question in self.questions if (question['category'] == stringCategory or not category) and (question['difficulty'] == difficulty or not difficulty) and (question['type'] == quizType or not quizType)][0:amount]

    
    def returnDecode(self, questions):
        return [{k:(b64decode(v).decode('utf-8') if isinstance(v, str) else [b64decode(x).decode('utf-8') for x in v]) for k,v in question.items()} for question in questions]


    async def question(self, amount=10, category=None, difficulty=None, quizType=None):
        if not(amount and isinstance(amount, int) and amount>0) or (category and (not isinstance(category, int) or not(0 < category < 25))) or (difficulty and difficulty not in self.difficulties) or (quizType and quizType not in self.types):
            raise InvalidParameters
            return

        if category:
            category += 8

        query = 'https://opentdb.com/api.php?amount=' + str(amount) + ('&category='+str(category) if category else '') + ('&difficulty='+difficulty if difficulty else '')  + ('&type='+quizType if quizType else '') + '&encode=base64' + '&token=' + self.token

        questions = await self.request(query)
        if not questions['results']:
            questions = self.cacheRequest(amount=amount, category=category, difficulty=difficulty, quizType=quizType)
        else:
            questions = questions['results']
            questions = self.returnDecode(questions)
        shuffle(questions)

        self.questions.extend(questions)
        return questions