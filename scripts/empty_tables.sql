-------------------------
-- Delete from staging --
-------------------------

delete from st_name_basics;
delete from st_title_principals;
delete from st_title_basics;
delete from st_title_ratings;

-----------------------
-- Delete from live --
-----------------------

delete from title;
delete from person;
delete from casting;