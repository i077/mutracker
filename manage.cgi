#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Manage artists</title>"
    print "<meta charset=\"UTF-8\">"
    print "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css\" integrity=\"sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu\" crossorigin=\"anonymous\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"
    print "<body>"
    print "<div class=\"ls\">"
    print "<h1>Remove an artist</h1>"
    print "<p>To unfollow an arist, click on them. \
             To unfollow everyone and start over, click <a href='main.cgi'>here</a>.</p>"
    print "Otherwise, go back to keep your list as is."
    print"</div>"

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
    print "<script src=\"https://code.jquery.com/jquery-3.4.1.slim.min.js\" integrity=\"sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js\" integrity=\"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js\" integrity=\"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6\" crossorigin=\"anonymous\"></script>"
    print "</body>"
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
