# short_url

1. Obtain ‘URL to be shortened’  from the user as an input via request arguments or via wtforms. Store this URL along with an identifier like a MD5 hash (Xinyao)
2. Stored the shortened URL in a database (use Postgres) (Xinjie)
3. while accessing the shortened URL, the user should be accessing {domain-name}/6BD7E4 ,and this should redirect the user to the original URL or should provide the user with a link to do so.(Xinjie)
4. Use GitHub as collaboration tool. Once code is pushed, setup the required configurations, connect Postgres and deploy the code to Heroku. Now, once the user tries to access  {app-name}.herokuapp.com/6BD7E4, they should be taken to the original URL.(TBC)
