# Selling the Cloud: data center ads and their energy & water claims

An R Shiny app that archives US and global data center ads (TV, YouTube, Facebook/Instagram, billboards, print) that make energy or water claims. For each ad it records:
- who the ad appears as, and who actually paid for it
- who saw it (place; age/gender for Meta issue ads)
- whether the claim can be fact-checked, with sources
- links to related lawsuits and investigations

## Run locally
```r
install.packages(c("shiny", "bslib", "DT", "htmltools", "wordcloud"))
shiny::runApp()
```

## Publish on Posit Connect Cloud
Connect Cloud -> Publish -> Shiny -> this repo, branch `main`, primary file `app.R`.
After changing packages, run `rsconnect::writeManifest(appFiles = c("app.R", list.files("data", full.names = TRUE)))` and commit `manifest.json`.

## Data
- `data/*.csv` is what the app reads.
- `build/` holds the scripts that generate the CSVs: run `python3 build/build_data.py data`, then `python3 build/enrich.py data`.
- Full ad transcripts are not included. The app quotes only short excerpts. `data/word_freq.csv` holds word counts from the transcripts, so rerunning `enrich.py` without them produces a smaller word cloud.
