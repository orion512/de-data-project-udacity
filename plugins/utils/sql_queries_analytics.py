class SqlQueriesAnalytics:
    """ Class for SQL queries for analytics """

    actors_avg_rating = ("""
        select
            p.primaryname,
            round(avg(t.averagerating)::numeric, 2),
            sum(t.numvotes)
        from person p
        join casting c on p.nconst = c.nconst
        join title t on c.tconst = t.tconst 
        where
            category in ('actress', 'actor') and
            t.titletype = 'movie' and 
            numvotes >= 5000
        group by p.nconst, p.primaryname
        having sum(t.numvotes) > 5000000
        order by avg(t.averagerating) desc
    """)

    actors_high_rated_movies = ("""
        with cte_high_movies as (
            select t.tconst 
            from title t
            where
                t.titletype = 'movie' and 
                t.averagerating >= 8.5 and 
                t.numvotes > 5000
        )
        select
            p.primaryname,
            count(*) num_movies
        from person p
        join casting c on p.nconst = c.nconst
        join cte_high_movies t on c.tconst = t.tconst 
        where category in ('actress', 'actor')
        group by p.nconst, p.primaryname
        order by count(*) desc
    """)

    actors_actresses = ("""
        with cte_gendres as (
            select c.category, t.averagerating, t.titletype 
            from title t
            join casting c on t.tconst = c.tconst
            where
                category in ('actress', 'actor') and 
                t.numvotes > 5000
        )
        select category, titletype, round(avg(averagerating)::numeric, 2)
        from cte_gendres
        group by category, titletype 
        order by titletype, category
    """)
