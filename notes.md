I built the URL shortener by using Python and Flask. The main features include shortening a URL, redirecting using a short code, and showing analytics like number of clicks and creation time.

For storing data, I used an in-memory dictionary since external databases were not allowed. I also used a lock from Python’s threading module to make sure it works safely when multiple users access it.

When a user sends a long URL, I first check if it’s valid using a regular expression. Then I generate a random 6-character short code and store the original URL with the code. When someone uses the short code, the app redirects to the original URL and increases the click count. There is also a stats endpoint to show the number of clicks and when it was created.

I wrote test cases using pytest to check all the important parts like shortening, redirecting, stats, and handling wrong inputs. All tests are passing.

I used AI tools to help with some parts like regex validation and thinking through test ideas, but I wrote all the final code myself and made sure I understood every part.
