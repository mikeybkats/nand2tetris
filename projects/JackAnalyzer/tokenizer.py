import io
from tokenTypes import TokenTypeTable, Token_Type


class JackTokenizer:
    def __init__(self, inputStreamOrFile):
        """
        Opens the input file/stream and gets ready to tokenize it.
        """
        if isinstance(inputStreamOrFile, io.TextIOBase):
            self._infile = inputStreamOrFile
        else:
            self._infile = open(inputStreamOrFile, mode='rt', encoding='utf-8')
        self._currentToken = ""
        self._tokenTypeTable = TokenTypeTable()

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
        firstChar = file.read(1)

        # check if the first character is line break or empty space
        # keep reading until a character is reached
        while firstChar == " " or firstChar == "\n":
            firstChar = file.read(1)
        char = firstChar

        # if the char is a symbol then return the token
        if self._tokenTypeTable.getTokenType(char) == Token_Type.SYMBOL:
            return char

        # if the char is not a symbol then build the token word
        while not tokenFoundOrEnd:
            # if a symbol is reached end the loop
            if (self._tokenTypeTable.getTokenType(char) == Token_Type.SYMBOL):
                # decrement the file reader back one space and break so the token can be read the next time the function is called
                self._infile.seek(prevReadLoc)
                tokenFoundOrEnd = True
                break
            if char == " " or char == "\n":
                tokenFoundOrEnd = True
                break
            if not char:
                tokenFoundOrEnd = True
                break
            else:
                token = token + char
                prevReadLoc = self._infile.tell()
                char = file.read(1)

        return token

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This method should only be called if hasMoreTokens() is true. Initially there is no current token.

        Returns:
            None
        """

        # if has more tokens
        if self.hasMoreTokens():
            # get the next token and assign it to current
            self._currentToken = self.getNextToken(self._infile)

    def tokenType(self):
        """
        Returns the type of the current token.

        Returns:
            TOKEN_TYPE enum
        """
        return self._tokenTypeTable.getTokenType(self._currentToken)

    def keyWord(self):
        """
        Returns the keyword which is the current token. Should be called only when the tokenType() is KEYWORD

        Returns:
            KEYWORD enum
        """
        if self.tokenType() == Token_Type.KEYWORD:
            return self._currentToken

    def symbol(self):
        """
        Returns the character which is the current token. Should be called only when tokenType() is SYMBOL 

        Returns:
            Char
        """
        if self.tokenType() == Token_Type.SYMBOL:
            return self._currentToken

    def identifier(self):
        """ 
        Returns the identifier which is the current token. Should be called only when tokenType() is IDENTIFIER

        Returns:
            String
        """
        if self.tokenType() == Token_Type.IDENTIFIER:
            return self._currentToken

    def intVal(self):
        """ 
        Return integer value of the current token. Should be called only when tokenType() is INT_CONST

        Returns:
            Int
        """
        if self.tokenType() == Token_Type.INT_CONST:
            return self._currentToken

    def stringVal(self):
        """
        Return the string value of the current token, without the double quotes. Should only be called when tokenType() is STRING_CONST

        Returns:
            String
        """
        if self.tokenType() == Token_Type.STRING_CONST:
            return self._currentToken.replace("\"", "").replace("'", "")
