#! /usr/bin/env -S awk -f
BEGIN {
	print "Content-type: text/html\n"
	print "<head>"
    print "<title>Album Details</title>"
    print "<meta charset=\"UTF-8\">"

	split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    get_details(query["id"])

	split(album_details["album_data"], album, /\|/)
	title = album[1]
	release_date = album[2]
	cover = album[3]
	artist = album[4]


	print "<img src=\""cover"\" width=\"250\" />"
	print "<p> "title" </p>"
	print "<p> "artist" </p>"
	split(release_date, release, /-/)
	year = release[1]
	print "<p> "year" </p>"
	print "<section class=\"listing\"><ol>"
	split(album_details["tracks"], track_list, /\n/)
	for(i = 2; i <= length(track_list); i++){
		split(track_list[i], line, /\|/)
		title = line[1]
		explicit = line[2]
		duration = int(line[3])
		min = int(duration/60)
		sec = duration%60
		if (sec < 10)
			sec = "0" sec

		if (explicit == "true"){
			print "<li>"title"  <font style=\"color:red\">&#127348;</font>         "min":"sec" </li>"
		}
		else {
			print "<li>"title"                     "min":"sec" </li>"
		}
	}
	print "</ol>"
}



func get_details(album_id,  album_name, genres, tracks){
	cmd = "curl -s http://api.deezer.com/album/"album_id" | jq -r '.title + \"|\" + \
        .release_date +  \"|\" + .cover_xl + \"|\" + .artist.name '"
	cmd | getline album_data
    close(cmd)

    cmd = "curl -s http://api.deezer.com/album/"album_id" | jq -r '(.genres.data[] | .name) '"
	cmd | getline genres
    close(cmd)
    gsub(/\n/ , "," , genres)

    cmd = "curl -s http://api.deezer.com/album/"album_id"/tracks | jq -r '.data[] | .title \
    	+  \"|\" + (.explicit_lyrics|tostring) + \"|\" + (.duration|tostring)'"
	while(cmd |getline l)
		tracks = tracks "\n" l
    close(cmd)
	album_details["album_data"] = album_data
	album_details["genres"] = genres
	album_details["tracks"] = tracks

}