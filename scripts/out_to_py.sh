# read tmp.output file

filename=$1

# Remove all rows between <<< generate and <<< solve
sed -i -e '/<<< generate/,/<<< solve/d' "$filename"

# Remove all rows starting with <<<
sed -i -e '/^<<<\s/d' "$filename"

# Remove spaces before [
sed -i 's/\s*\[/[/g' "$filename"

# Replace spaces between brackets with commas
sed -i -E ':a; s/\[([^][]*)\s+([^][]*)\]/[\1,\2]/g; ta' "$filename"

# Add indentation and remove trailing commas
sed -i -E '/\[/{N;s/\n/ /;s/(, )+/,\n    /g}' "$filename"
sed -i 's/,\s*]/]/g' "$filename"

# Convert OBJECTIVE line to objective assignment
sed -i -E 's/OBJECTIVE: (.*)/objective = \1/g' "$filename"

# save
cp $filename $2