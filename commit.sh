git add *
git commit -m "Commit Script"
git push
git push heroku main
heroku logs --tail >> log.log