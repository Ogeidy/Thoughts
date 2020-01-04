SQL_CREATE_THOUGHT_TABLE = '''CREATE TABLE IF NOT EXISTS Thought (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Description TEXT
                        );'''
SQL_CREATE_THOUGHTS_TABLE = '''CREATE TABLE IF NOT EXISTS Thoughts (
                            Id INTEGER PRIMARY KEY,
                            ThoughtId INTEGER NOT NULL,
                            Date DATE,
                            FOREIGN KEY (ThoughtId) REFERENCES Thought (Id)
                        );'''
SQL_CREATE_TAG_TABLE = '''CREATE TABLE IF NOT EXISTS Tag (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL
                        );'''
SQL_CREATE_THOUGHTTAG_TABLE = '''CREATE TABLE IF NOT EXISTS ThoughtTag (
                            ThoughtId INTEGER NOT NULL,
                            TagId INTEGER NOT NULL,
                            FOREIGN KEY (ThoughtId) REFERENCES Thoughts (Id),
                            FOREIGN KEY (TagId) REFERENCES Tag (Id),
                            UNIQUE (ThoughtId, TagId)
                        );'''