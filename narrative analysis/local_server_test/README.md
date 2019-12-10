# Set up local testing server

### The problem with testing local files

Some local html files won't run without a local testing server because..

- **They feature asynchronous requests.** Some browsers (including Chrome) will not run async requests 
(see Fetching data from the server) if you just run the example from a local file. This is 
because of security restrictions (for more on web security, read Website security).

- **They feature a server-side language.** Server-side languages (such as PHP or Python) require a special server 
to interpret the code and deliver the results.

### How to create a local server 
1. Open the terminal(macOS)
2. navigate to the directory that the files are inside
```
# In Python3
python3 -m http.server 8080

# 8080 is one of the ports, we can also choose another port if port 8080 is being used currently (e.g. python3 -m http.server 8000)
# Then we can go to this server by going to the URL localhost:80080

```
