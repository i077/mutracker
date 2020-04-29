#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Music Release Tracker</title>"
    print "<meta charset=\"UTF-8\">"
    print "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css\" integrity=\"sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu\" crossorigin=\"anonymous\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"
    print "<body>"
    print "<div class=\"ls\">"
    print "<h1>Music Release Tracker</h1>"

    split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    # Clean up IDs
    gsub(/%2C/,",",query["ids"])
    # Remove trailing comma from IDs
    gsub(/,$/,"",query["ids"])
    n_artists = split(query["ids"], ids, /,/)

    print "<form method='GET' action='search.cgi'>"
    print "<p>Follow a new artist: "
    print "<input name='artist_q' autocomplete='off'/> <input type='submit' value='Search'/></p>"
    print "<input type='hidden' name='ids' value=\""query["ids"]"\"/>"
    print "</form>"

    print "<p>Artists you're following: "n_artists". \
          <a href='manage.cgi?ids="query["ids"]"'>Manage</a></p>"
    print "</div>"          
    print "<hr/>"
    print "<div class=\"ls\">"
    print "<h1>Latest Releases</h1>"
    print "<p>Protip: To save your list, just bookmark this page.</p>"
    print "</div>"
    print "<section class=\"listing\"><ul>"

    for (i in ids) {
        raw_album_list = raw_album_list "\n" releases(ids[i])
    }
    # Guard against bashisms
    gsub(/"/, "\\\"", raw_album_list)
    gsub(/\$/, "\\$", raw_album_list)
    cmd = "echo \""raw_album_list"\" | sort -r"
    n = 0
    while (cmd | getline l) {
        if (l != "") {
            album_list[n] = l
            n++
        }
    }
    close(cmd)

    # Print each album
    for (i = 0; i < n; i++) {
        split(album_list[i], album, /\|/)
        reldate = album[1]
        title = album[2]
        artist = album[3]
        cover = album[4]
        id = album[5]

        # Parse date to a nicer format
        cmd = "date -d'"reldate"' +'%B %-d, %Y'"
        while (cmd | getline l)
            humandate = l
        close(cmd)

        print "<li><a href='album_details.cgi?id="id"' ><img src=\""cover"\" width=\"250\" /></a><br/>\
              <p class=\"albuminfo\"><strong>"title"</strong></p>\
              <p>"artist"</p>\
              <p><em>Released "humandate"</em></p><br/></li>"
    }
    print "</ul></section>"
    print "<script src=\"https://code.jquery.com/jquery-3.4.1.slim.min.js\" integrity=\"sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js\" integrity=\"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo\" crossorigin=\"anonymous\"></script>"
    print "<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js\" integrity=\"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6\" crossorigin=\"anonymous\"></script>"
    print "</body>"
}

func releases(artist,  ar_resp, al_resp, artist_name, albums) {
    # Get artist name
    cmd = "curl -s http://api.deezer.com/artist/"artist" | jq -r .name"
    cmd | getline artist_name
    close(cmd)

    # Get albums for this artist
    cmd = "curl -s http://api.deezer.com/artist/"artist"/albums | jq -r '.data[] | \
        .release_date + \"|\" + .title + \"|"artist_name"|\" + .cover_big + \"|\" + (.id|tostring) '"
    while (cmd | getline l)
        albums = albums "\n" l
    close(cmd)
    return substr(albums, 1, length(albums)-1)
}


# vim: set ft=awk:
