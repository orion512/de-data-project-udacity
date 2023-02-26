class SqlQueriesLoad:
    """ Class for SQL queries to load data from staging """

    casting_insert = ("""
        INSERT INTO casting (tconst, ordering, nconst, category, job, characters)
        SELECT
            tconst,
            ordering::INT,
            nconst,
            category,
            NULLIF(job,'\\N') AS job, 
            REPLACE(REPLACE(NULLIF(characters,'\\N'), '[', '{'), ']', '}')::TEXT[] AS characters
        FROM st_title_principals
        ON CONFLICT (tconst, ordering) DO update set
            category = EXCLUDED.category,
            job = EXCLUDED.job,
            characters = EXCLUDED.characters
    """)

    person_insert = ("""
        INSERT INTO person
        SELECT
            nconst,
            primaryName,
            NULLIF(birthYear, '\\N')::INT,
            NULLIF(deathYear, '\\N')::INT,
            ('{' || primaryProfession || '}')::TEXT[] AS primaryProfession,
            ('{' || NULLIF(knownForTitles, '\\N') || '}')::TEXT[] AS knownForTitles
        FROM st_name_basics
        ON CONFLICT (nconst) DO update set
            primaryName = EXCLUDED.primaryName,
            deathyear = EXCLUDED.deathYear,
            knownForTitles = EXCLUDED.knownForTitles,
            primaryProfession = EXCLUDED.primaryProfession
    """)

    title_insert = ("""
        INSERT INTO title
        select
            stb.tconst,
            stb.titleType,
            stb.primaryTitle,
            stb.originalTitle,
            stb.isAdult::INT,
            NULLIF(stb.startYear, '\\N')::INT as startYear,
            NULLIF(stb.endYear, '\\N')::INT as endYear,
            NULLIF(stb.runtimeMinutes, '\\N')::INT as runtimeMinutes,
            ('{' || NULLIF(stb.genres, '\\N') || '}')::TEXT[] AS genres,
            str.averageRating::FLOAT,
            str.numVotes::INT
        from st_title_basics stb 
        left join st_title_ratings str on stb.tconst = str.tconst
        ON CONFLICT (tconst) DO update set
            endYear = EXCLUDED.endYear,
            averageRating = EXCLUDED.averageRating,
            numVotes = EXCLUDED.numVotes
    """)
