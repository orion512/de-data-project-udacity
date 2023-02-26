class SqlQueriesInit:

    st_title_basics_create = ("""
        CREATE TABLE st_title_basics (
            tconst TEXT,
            titleType TEXT,
            primaryTitle TEXT,
            originalTitle TEXT,
            isAdult TEXT,
            startYear TEXT,
            endYear TEXT,
            runtimeMinutes TEXT,
            genres TEXT
        );
    """)

    st_title_ratings_create = ("""
        CREATE TABLE st_title_ratings (
            tconst TEXT,
            averageRating TEXT,
            numVotes TEXT
        );
    """)

    st_title_principals_create = ("""
        CREATE TABLE st_title_principals (
            tconst TEXT,
            ordering TEXT,
            nconst TEXT,
            category TEXT,
            job TEXT,
            characters TEXT
        ); 
    """)

    st_name_basics_create = ("""
        CREATE TABLE st_name_basics (
            nconst TEXT,
            primaryName TEXT,
            birthYear TEXT,
            deathYear TEXT,
            primaryProfession TEXT,
            knownForTitles TEXT
        );
    """)

    title_create = ("""
        CREATE TABLE title (
            tconst TEXT PRIMARY KEY,
            titleType TEXT NOT NULL,
            primaryTitle TEXT,
            originalTitle TEXT,
            isAdult INT,
            startYear INT,
            endYear INT,
            runtimeMinutes INT,
            genres TEXT,
            averageRating FLOAT,
            numVotes INT
        );
    """)

    casting_create = ("""
        CREATE TABLE casting (
            id SERIAL PRIMARY KEY,
            tconst TEXT NOT NULL,
            ordering INT NOT NULL,
            nconst TEXT NOT NULL,
            category TEXT NOT NULL,
            job TEXT,
            characters TEXT[],
            UNIQUE (tconst, ordering)
        );
    """)

    person_create = ("""
        CREATE TABLE person (
            nconst TEXT PRIMARY KEY,
            primaryName TEXT,
            birthYear INT,
            deathYear INT,
            primaryProfession TEXT[],
            knownForTitles TEXT[]
        );
    """)
