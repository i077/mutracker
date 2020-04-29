#! /usr/bin/env -S awk -f
BEGIN {
	print "Content-type: text/html\n"
	print "<head>"
    print "<title>Album Details</title>"
    print "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css\" integrity=\"sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu\" crossorigin=\"anonymous\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "<meta charset=\"UTF-8\">"
    print "</head>"
    print "<body>"

	split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    get_details(query["id"])

	split(album_details["album_data"], album, /\|/)
	title = album[1]
	release_date = album[2]
	cover = album[3]
	artist = album[4]


	print "<div class = \"container-fluid\">"
		print "<div class = \"row justify-content-start\">"

			print "<div class = \"col-sm-4\">"
			print "<img src=\""cover"\" width=\"250\" />"
			print "</div>"

			print "<div class=\"col-sm-6\">"
			print "<h1><strong> "title" </strong></h1>"
			print "<p><strong> "artist" </strong></p>"
			split(release_date, release, /-/)
			year = release[1]
			print "<p><strong> "year" </strong></p>"

			print "<section> <ol class=\"twocol\">"
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
					print "<li>"title"  <font style=\"color:red\">&#127348;</font>         <strong class=\"right\">"min":"sec"</strong> </li>"
				}
				else {
					print "<li> "title" <strong class=\"right\"> "min":"sec" </strong> </li>"
			}
			}
			print "</ol>"
			print "</div>"

		print "</div>"
	print"</div>"

	print "<script src=\"https://code.jquery.com/jquery-3.4.1.slim.min.js\" integrity=\"sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js\" integrity=\"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js\" integrity=\"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6\" crossorigin=\"anonymous\"></script>"
	print "</body>"
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
