import io
from TokenTypes import TokenTypeTable, Token_Type


class JackTokenizer:
    def __init__(self, inputStreamOrFile):
        """
        Opens the input file/stream and gets ready to tokenize it.
        """
        if isinstance(inputStreamOrFile, io.TextIOBase):
            self._infile = inputStreamOrFile
        else:
            self._infile = open(inputStreamOrFile, mode='rt', encoding='utf-8')

        self.strip_comments_from_infile()
        self._currentToken = ""
        self._tokenTypeTable = TokenTypeTable()
        self._prevTokenLoc = 0

    @property
    def currentToken(self):
        return self._currentToken

    @currentToken.setter
    def currentToken(self, new):
        self._currentToken = new

    @property
    def prev_token_loc(self):
        return self._prevTokenLoc

    def has_more_tokens(self):
        """
        checks to see if the input contains more tokens

        Returns:
            boolean
        """
        current_location = self._infile.tell()

        file_contents = self._infile.read()
        has_more_tokens = False if not file_contents else True
        if file_contents.isspace():
            has_more_tokens = False

        self._infile.seek(current_location)
        return has_more_tokens

    @property
    def infile(self):
        return self._infile

    def strip_comments_from_infile(self):
        replacement = io.StringIO()

        for line in self._infile:
            changes = line.split("//", 1)[0].rstrip().lstrip()
            if len(changes) > 1:
                if changes[:3] == "/**":
                    changes = changes.split("/*", 1)[0].split("*/", 1)[0]
                elif changes[:2] != "/*" and changes[0] == "*":
                    changes = changes.split("*", 1)[0]
            replacement.write(changes)

        self._infile = replacement
        self._infile.seek(0)
        return replacement

    def get_next_token(self, file):
        """
        Reads one char at a time from the file to build the next token. Stops when it sees whitespace. 

        Arg1:
            FileStream

        Returns:
            string
        """

        token = ""
        token_found_or_end = False
        first_char = file.read(1)

        # check if the first character is line break or empty space
        # keep reading until a character is reached
        while first_char == " " or first_char == "\n":
            first_char = file.read(1)
        char = first_char

        # if the char is a symbol then return the token
        if char and self._tokenTypeTable.get_token_type(char) == Token_Type.SYMBOL:
            return char

        # if the char is not a symbol then build the token word
        while not token_found_or_end:
            # if a symbol is reached end the loop
            if char == "\"" or char == "\'":
                # if a quotation is reached build the sentence
                char = file.read(1)
                sentence = ""
                while char != "\"" or char == "\'":
                    sentence = sentence + char
                    char = file.read(1)
                return "\"" + sentence + "\""
            if char and self._tokenTypeTable.get_token_type(char) == Token_Type.SYMBOL:
                # decrement the file reader back one space and break so the token
                # can be read the next time the function is called
                self._infile.seek(prev_read_loc)
                token_found_or_end = True
                break
            if char == " " or char == "\n":
                token_found_or_end = True
                break
            if not char:
                token_found_or_end = True
                break
            else:
                token = token + char
                prev_read_loc = self._infile.tell()
                char = file.read(1)

        return token

    def tell(self):
        return self._infile.tell()

    def look_ahead(self):
        """returns the next token"""
        prev_token = self._currentToken
        self.advance()

        next_token = self._currentToken
        self._infile.seek(self.prev_token_loc)
        self._currentToken = prev_token

        return next_token

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This method should only be called if hasMoreTokens() is true. Initially there is no current token.

        Returns:
            None
        """

        # if has more tokens
        if self.has_more_tokens():
            self._prevTokenLoc = self._infile.tell()
            # get the next token and assign it to current
            self._currentToken = self.get_next_token(self._infile)

    def token_type(self):
        """
        Returns the type of the current token.

        Returns:
            TOKEN_TYPE enum
        """
        return self._tokenTypeTable.get_token_type(self._currentToken)

    def key_word(self):
        """
        Returns the keyword which is the current token. Should be called only when the tokenType() is KEYWORD

        Returns:
            KEYWORD enum
        """
        if self.token_type() == Token_Type.KEYWORD:
            return self._currentToken

    def symbol(self):
        """
        Returns the character which is the current token. Should be called only when tokenType() is SYMBOL 

        Returns:
            Char
        """
        if self.token_type() == Token_Type.SYMBOL:
            return self._currentToken

    def identifier(self):
        """ 
        Returns the identifier which is the current token. Should be called only when tokenType() is IDENTIFIER

        Returns:
            String
        """
        if self.token_type() == Token_Type.IDENTIFIER:
            return self._currentToken

    def int_val(self):
        """ 
        Return integer value of the current token. Should be called only when tokenType() is INT_CONST

        Returns:
            Int
        """
        if self.token_type() == Token_Type.INT_CONST:
            return self._currentToken

    def string_val(self):
        """
        Return the string value of the current token, without the double quotes. Should only be called when tokenType() is STRING_CONST

        Returns:
            String
        """
        if self.token_type() == Token_Type.STRING_CONST:
            return self._currentToken.replace("\"", "").replace("'", "")
