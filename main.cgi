#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Music Release Tracker</title>"
    print "<meta charset=\"UTF-8\">"
    print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">"
    print "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\" integrity=\"sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh\" crossorigin=\"anonymous\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"

    print "<body>"
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

    print "<hr/>"
    print "<h1>Latest Releases</h1>"
    print "<p>Protip: To save your list, just bookmark this page.</p>"
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
        explicit = album[6] == "true"

        # Parse date to a nicer format
        cmd = "date -d'"reldate"' +'%B %-d, %Y'"
        while (cmd | getline l)
            humandate = l
        close(cmd)

        print "<li><a onclick='document.getElementById(\"albumModal-"id"\").style.display=\"block\"' id='cover-"id"'><img src=\""cover"\" width=\"250\"/></a><br/>\
              <p><strong>"title"</strong>"
        if (explicit)
            print " <font style=\"color:red\">&#127348;</font>"
        print "</p><p>"artist"</p>\
              <p><em>Released "humandate"</em></p><br/></li>"
        print "<div id='albumModal-"id"' class='modal'><div class='modal-content'>"
        print "<div class='modal-body'>"
        print "<iframe src='album_details.cgi?id="id"' loading='lazy'\
              frameborder='0' width='100%' height='400px'></iframe>"
        print "</div></div></div>"
        print "<script>\n\
              window.addEventListener(\"click\", function(event) {\n\
                  var modal = document.getElementById(\"albumModal-"id"\");\n\
                  if (event.target == modal) {\n\
                      modal.style.display = \"none\";\n\
                  }\n\
              })\n\
</script>"
    }
    print "</ul></section>"


    print "</body>"
}

func releases(artist,  ar_resp, al_resp, artist_name, albums) {
    # Get artist name
    cmd = "curl -s http://api.deezer.com/artist/"artist" | jq -r .name"
    cmd | getline artist_name
    close(cmd)

    # Get albums for this artist
    cmd = "curl -s http://api.deezer.com/artist/"artist"/albums | jq -r '.data[] | \
        .release_date + \"|\" + .title + \"|"artist_name"|\" + .cover_big + \"|\" + (.id|tostring) + \"|\" + (.explicit_lyrics|tostring) '"
    while (cmd | getline l)
        albums = albums "\n" l
    close(cmd)
    return substr(albums, 1, length(albums)-1)
}

# vim: set ft=awk:
