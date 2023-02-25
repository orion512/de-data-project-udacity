class SqlQueriesInit:


CREATE TABLE st_title_ratings (
	tconst TEXT,
	averageRating TEXT,
	numVotes TEXT
);

CREATE TABLE st_title_principals (
	tconst TEXT,
	ordering TEXT,
	nconst TEXT,
	category TEXT,
	job TEXT,
	characters TEXT
); 

CREATE TABLE st_name_basics (
	nconst TEXT,
	primaryName TEXT,
	birthYear TEXT,
	deathYear TEXT,
	primaryProfession TEXT,
	knownForTitles TEXT
);

/* Live Tables */

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

CREATE TABLE person (
	nconst TEXT PRIMARY KEY,
	primaryName TEXT,
	birthYear INT,
	deathYear INT,
	primaryProfession TEXT[],
	knownForTitles TEXT[]
);

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
        LIMIT 1000
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
        limit 1000
    """)
