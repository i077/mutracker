all:
	mkdir out
	for f in $(shell ls ./*.cgi); do \
		sed 's_/usr/bin/env -S awk -f_/usr/bin/awk -f_' $${f} > out/$${f}; \
		scp out/$${f} rev24@eecslab-16.case.edu:~/public_html/cgi-bin/proj3/; \
	done
	scp main.css rev24@eecslab-16.case.edu:~/public_html/
	rm -rf out