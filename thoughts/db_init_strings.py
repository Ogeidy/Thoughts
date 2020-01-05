SQL_CREATE_THOUGHT_TABLE = '''CREATE TABLE IF NOT EXISTS Thought (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Description TEXT,
                            UNIQUE (Name)
                        );'''
SQL_CREATE_MENTION_TABLE = '''CREATE TABLE IF NOT EXISTS Mention (
                            Id INTEGER PRIMARY KEY,
                            ThoughtId INTEGER NOT NULL,
                            Date TEXT DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (ThoughtId) REFERENCES Thought (Id)
                        );'''
SQL_CREATE_TAG_TABLE = '''CREATE TABLE IF NOT EXISTS Tag (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            UNIQUE (Name)
                        );'''
SQL_CREATE_MENTIONTAG_TABLE = '''CREATE TABLE IF NOT EXISTS MentionTag (
                            MentionId INTEGER NOT NULL,
                            TagId INTEGER NOT NULL,
                            FOREIGN KEY (MentionId) REFERENCES Mention (Id),
                            FOREIGN KEY (TagId) REFERENCES Tag (Id),
                            UNIQUE (MentionId, TagId)
                        );'''