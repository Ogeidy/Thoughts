SQL_CREATE_THOUGHT_TABLE = '''CREATE TABLE IF NOT EXISTS thought (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT,
                            UNIQUE (name)
                        );'''
SQL_CREATE_MENTION_TABLE = '''CREATE TABLE IF NOT EXISTS mention (
                            id INTEGER PRIMARY KEY,
                            thought_id INTEGER NOT NULL,
                            date TEXT DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (thought_id) 
                                REFERENCES thought (id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE
                        );'''
SQL_CREATE_TAG_TABLE = '''CREATE TABLE IF NOT EXISTS tag (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL UNIQUE
                        );'''
SQL_CREATE_MENTIONTAG_TABLE = '''CREATE TABLE IF NOT EXISTS mention_tag (
                            mention_id INTEGER,
                            tag_id INTEGER,
                            PRIMARY KEY (mention_id, tag_id),
                            FOREIGN KEY (mention_id) 
                                REFERENCES mention (id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE,
                            FOREIGN KEY (tag_id) 
                                REFERENCES tag (id)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE
                        );'''