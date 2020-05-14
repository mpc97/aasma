all:
	python3 project.py > project1.txt
	chmod 755 project1.txt

clean:
	rm -f project1.txt