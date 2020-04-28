#! /usr/bin/env -S awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<head>"
    print "<title>Music Release Tracker</title>"
    print "<meta charset=\"UTF-8\">"
    print "<link rel=\"stylesheet\" href=\"../../main.css\" />"
    print "</head>"

    split(ENVIRON["QUERY_STRING"], dd, /&/)
    for (i in dd) { split(dd[i], field, /=/); query[field[1]] = field[2] }

    # Clean up IDs
    gsub(/%2C/,",",query["ids"])

    print "<h1>Results for '"query["artist_q"]"'</h1>"
    print "<p>Click an artist name to follow them.</p>"
    print "<br/>"
    dz_artist_search(query["artist_q"])
}

# Perform a search through Deezer's API for an artist name,
# and print a list of the results.
func dz_artist_search(artist,  resp, results, result) {
    # Get API response from Deezer
    gsub(/'/, "\\'", artist)
    cmd = "curl -s 'http://api.deezer.com/search/artist?q="artist"' | jq -r '.data[] | \
        (.id|tostring) + \"|\" + .name + \"|\" + .picture_medium'"
    num_res = 0
    while (cmd | getline l) {
        results[num_res] = l
        num_res++
    }
    close(cmd)

    # Print results
    print "<section class=\"listing\"><ul>"
    for (i = 0; i < num_res; i++) {
        split(results[i], result, /\|/)
        id = result[1]
        name = result[2]
        pic = result[3]
        print "<li><a href=\"main.cgi?ids="id","query["ids"]"\"><img src="pic" width=\"200\" /></a><br/><p>"name"</p><br/></li>"
    }
    print "</ul></section>"
}

# vim: set ft=awk:
