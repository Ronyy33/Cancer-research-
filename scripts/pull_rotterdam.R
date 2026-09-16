# Pulls the real Rotterdam breast cancer cohort directly from R's own
# `survival` package (the authoritative source - not a secondhand
# mirror) and exports it to CSV for use in the Python pipeline.
#
# Run: Rscript scripts/pull_rotterdam.R

data(cancer, package = "survival")

stopifnot(exists("rotterdam"))

out_path <- "data/raw/rotterdam_raw.csv"
write.csv(rotterdam, out_path, row.names = FALSE)

cat("Rotterdam dataset pulled from survival package.\n")
cat("N =", nrow(rotterdam), "\n")
cat("Columns:", paste(colnames(rotterdam), collapse = ", "), "\n")
cat("Saved to", out_path, "\n")
