class JackTokenizer:
    def __init__(self, inputStreamOrFile):
        """
        Opens the input file/stream and gets ready to tokenize it.
        """
        self._infile = open(inputStreamOrFile, mode='rt', encoding='utf-8')
        self._currentToken = None

    @property
    def currentToken(self):
        return self._currentToken

    def hasMoreTokens(self):
        """
        checks to see if the input contains more tokens

        Returns:
            boolean
        """
        currentLocation = self._infile.tell()
        fileContents = self._infile.read()
        hasMoreTokens = True if fileContents else False
        self._infile.seek(currentLocation)
        return hasMoreTokens

    def getNextToken(self, file):
        """
        Reads one char at a time from the file to build the next token. Stops when it sees whitespace. 

        Arg1:
            FileStream

        Returns:
            string
        """

        token = ""
        tokenFoundOrEnd = False
        while not tokenFound:
            char = file.read(1)
            if char == " ":
                tokenFoundOrEnd = True
            if not char:
                tokenFoundOrEnd = True
            token = token + char

        return token

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This method should only be called if hasMoreTokens() is true. Initially there is no current token.

        Returns:
            None
        """

        # while hasMoreTokens
        with self._infile as file:
            while True:
                token = self.getNextToken(file)
                self.currentToken = self.getNextToken(line)

            # self._infile.readline()
            # advance to the next token
        return None

    def tokenType(self):
        """
        Returns the type of the current token.

        Returns:
            TOKEN_TYPE enum
        """

    def keyWord(self):
        """
        Returns the keyword which is the current token. Should be called only when the tokenType() is KEYWORD

        Returns:
            KEYWORD enum
        """

    def symbol(self):
        """
        Returns the character which is the current token. Should be called only when tokenType() is SYMBOL 

        Returns:
            Char
        """

    def identifier(self):
        """ 
        Returns the identifier which is the current token. Should be called only when tokenType() is IDENTIFIER

        Returns:
            String
        """

    def intVal(self):
        """ 
        Return integer value of the current token. Should be called only when tokenType() is INT_CONST

        Returns:
            Int
        """

    def stringVal(self):
        """
        Return the string value of the current token, without the double quotes. Should only be called when tokenType() is STRING_CONST

        Returns:
            String
        """
