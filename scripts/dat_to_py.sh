# read the data from the model/thesis-4.dat
# remove all comments (rows starting with // or rows between /* and */) and all semicolons
# write the result to dat_file.py

cat $1 | sed -e 's/\/\/.*$//' -e '/\/\*/,/\*\//d' -e 's/;//' > $2
