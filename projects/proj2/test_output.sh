dir1="output_solution"
dir2="output"

# Check if directories exist
if [ ! -d "$dir1" ] || [ ! -d "$dir2" ]; then
  echo "One or both directories do not exist."
  exit 1
fi

# Iterate through files in the first directory
for file1 in "$dir1"/*; do
  # Extract the file name
  file_name=$(basename "$file1")
  
  # Check if the file exists in the second directory
  if [ -e "$dir2/$file_name" ]; then
    # Run diff on the files
    echo "~~~~ diffs for $file1~~~~"
    diff -B "$file1" "$dir2/$file_name"
  else
    echo "File $file_name does not exist in the second directory."
  fi
done

