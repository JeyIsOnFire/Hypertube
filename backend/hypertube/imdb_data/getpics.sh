# https://www.omdbapi.com
#
# omdb api key : f5ffda2e
#
# max 1000 requetes / jour
#
for id in $(head -n 5 data/name.basics.tsv | cut -f6 | tr ',' '\n'); do
  curl "http://www.omdbapi.com/?i=$id&apikey=f5ffda2e" | jq '.Title, .Poster'
done

