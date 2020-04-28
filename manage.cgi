#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Manage artists</title>"
    print "<meta charset=\"UTF-8\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"
    print "<h1>Remove an artist</h1>"
    print "<p>To unfollow an arist, click on them. \
             To unfollow everyone and start over, click <a href='main.cgi'>here</a>.</p>"
    print "Otherwise, go back to keep your list as is."

    split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    # Clean up IDs
    gsub(/%2C/,",",query["ids"])
    
    # Remove trailing comma from IDs
    gsub(/,$/,"",query["ids"])
    n_artists = split(query["ids"], ids, /,/)

    print "<section class=\"listing\"><ul>"
    for (i in ids) {
        removed_id = ""
        for (j in ids) {
            if (i != j)
                removed_id = ids[j] "," removed_id
        }
        artist_remove_entry(ids[i], removed_id)
    }
    print "</ul></section>"
}

func artist_remove_entry(artist, removed_id,  artist_data, result) {
    gsub(/'/, "\\'", artist)
    cmd = "curl -s 'http://api.deezer.com/artist/"artist"' | jq -r '.name + \"|\" + .picture_medium'"
    while (cmd | getline l) {
        artist_data = l
    }
    close(cmd)

    # Print artist info
    split(artist_data, result, /\|/)
    name = result[1]
    pic = result[2]
    print "<li><a href=\"main.cgi?ids="removed_id"\"><img src="pic" width=\"200\" /></a><br/><p>"name"</p><br/></li>"
}
# vim: set ft=awk:
