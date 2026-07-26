#' Figure 4: odds-implied teammate gaps compared with the historical threshold
#'
#' @param gaps output from teammate_gaps()
#' @param threshold upper endpoint from second_driver_ci()
#' @param file output PNG path
plot_teammate_gaps <- function(
    gaps,
    threshold,
    file = "figures/04_teammate_gaps.png"
) {
  gaps <- gaps[order(-gaps$gap), , drop = FALSE]
  labels <- paste0(gaps$leading_driver, "  (", gaps$team, ")")
  cols <- ifelse(gaps$outperforms_car, "#C8102E", "grey65")

  png(file, width = 1800, height = 1050, res = 180)
  op <- par(mar = c(5, 15, 3, 2), xpd = NA)
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  bp <- barplot(
    rev(gaps$gap),
    horiz = TRUE,
    col = rev(cols),
    border = NA,
    names.arg = rev(labels),
    las = 1,
    cex.names = 0.78,
    xlim = c(0, max(gaps$gap) * 1.08),
    xlab = "Expected-position gap to team-mate (odds-implied)",
    main = "Which drivers outperform their car?"
  )

  abline(v = threshold, lty = 2, lwd = 2)
  text(
    threshold,
    max(bp),
    pos = 4,
    cex = 0.8,
    labels = sprintf("car-only threshold = %.3f", threshold)
  )

  invisible(file)
}
