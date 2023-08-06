for f in *.ipynb
do
  jupyter nbconvert --to notebook --execute "$f" --output "$f"
done