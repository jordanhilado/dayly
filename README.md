# Dayly

Dayly is an online personal management web application service. It allows users to manage their tasks, notes, and calendar. Included within the homepage of Dayly is a dashboard that includes, live weather, stock information, and news.

# Build

you can build the container with:

```bash
docker build -t dayly .
```

and run with:

```bash
docker run --name dayly --rm -it -p 5000:5000 dayly
```

and to access go to [](http://localhost:5000) your browser 

## Build Disclaimer
The build is from a `fedora` image, if you want a production build please use a different build

## Sources
* Bootstrap: https://getbootstrap.com/
* Favicon: https://favicon.io/
* Elfsight: https://elfsight.com/ 
* Trading View: https://www.tradingview.com/
* RSS Feed Widget: http://www.rssfeedwidget.com/
* Weather Widget IO: https://weatherwidget.io/

# TODO
[ ] decide if [](Dayly/__pycache__/application.cpython-38.pyc) and [](Dayly/__pycache__/helpers.cpython-38.pyc and b/Dayly/__pycache__/helpers.cpython-38.pyc) should be ignored in a `.gitignore`
[ ] decide how to save creds not inside the github repo [](Dayly/final.db`)
