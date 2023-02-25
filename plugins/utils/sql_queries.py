class SqlQueries:
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
        LIMIT 1000;
    """)

    person_insert = ("""
        INSERT INTO person
        SELECT
            nconst,
            primaryName,
            NULLIF(birthYear, '\\N')::INT,
            NULLIF(deathYear, '\\N')::INT,
            ('{' || primaryProfession || '}')::TEXT[] AS primaryProfession,
            ('{' || knownForTitles || '}')::TEXT[] AS knownForTitles
        FROM st_name_basics
        LIMIT 1000
    """)

    title_insert = ("""
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
        limit 1000
    """)
