class Tokenizer:
    def __init__(self, source, path):
        self._source = source
        self._path = path
        self._create_tokens()

    def _create_tokens(self):
        self._initialize_state()
        while self._index < len(self._source):
            self._process_character()

    def _initialize_state(self):
        self._line = 1
        self._column = 1
        self._index = 0

    def _process_character(self):
        c = self._source[self._index]

