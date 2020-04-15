#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Music Release Tracker</title>"
    print "<meta charset=\"UTF-8\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"
    print "<h1>Music Release Tracker</h1>"
    print "<p>Type an artist's name to search for.</p>"

    split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    # Clean up IDs
    gsub(/%2C/,",",query["ids"])

    print "<form method='GET' action='search.cgi'>"
    print "<p>Search for an artist "
    print "<input name='artist_q'/> <input type='submit' value='Search'/></p>"
    print "<input type='hidden' name='ids' value=\""query["ids"]"\"/>"
    print "</form>"

    print "<hr/>"
    print "<h1>Latest Releases</h1>"
    print "<p>Protip: To save your list, just bookmark this page.</p>"
    print "<section class=\"listing\"><ul>"
    # Remove trailing comma from IDs
    gsub(/,$/,",0",query["ids"])
    split(query["ids"], ids, /,/)
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

        # Parse date to a nicer format
        cmd = "date -d'"reldate"' +'%B %d, %Y'"
        while (cmd | getline l)
            humandate = l
        close(cmd)

        print "<li><img src=\""cover"\" width=\"250\" /></a><br/>\
              <p><strong>"title"</strong></p>\
              <p>"artist"</p>\
              <p><em>Released "humandate"</em></li>"
    }
    print "</ul></section>"
}

func releases(artist,  ar_resp, al_resp, artist_name, albums) {
    # Get artist name
    cmd = "curl -s http://api.deezer.com/artist/"artist" > /tmp/iah13_resp.out"
    system(cmd)
    cmd = "cat /tmp/iah13_resp.out | jq -r .name"
    cmd | getline artist_name
    close(cmd)
    system("rm /tmp/iah13_resp.out")

    # Get albums for this artist
    cmd = "curl -s http://api.deezer.com/artist/"artist"/albums > /tmp/iah13_resp.out"
    system(cmd)
    cmd = "cat /tmp/iah13_resp.out | jq -r '.data[] | \
        .release_date + \"|\" + .title + \"|\" + \""artist_name"\" + \"|\" + .cover_big'"
    while (cmd | getline l)
        albums = l "\n" albums
    system("rm /tmp/iah13_resp.out")
    return substr(albums, 1, length(albums)-1)
}

# vim: set ft=awk:
