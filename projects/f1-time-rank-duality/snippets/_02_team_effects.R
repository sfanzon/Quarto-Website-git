#' Figure 2: constructor effects from the selected 2022 regression
#'
#' @param model fitted model returned by select_models()$stepwise
#' @param file output PNG path
plot_team_effects <- function(
    model,
    file = "figures/02_team_effects.png"
) {
  tab <- regression_table(model)
  model_terms <- c(
    "RedBull", "Mercedes", "Ferrari", "McLaren", "Alpine", "AstonMartin"
  )
  display_names <- c(
    RedBull = "RedBull",
    Mercedes = "Mercedes",
    Ferrari = "Ferrari",
    McLaren = "Mclaren",
    Alpine = "Alpine",
    AstonMartin = "AstonMartin"
  )

  rows <- match(model_terms, tab$term)
  est <- tab$estimate[rows]
  se <- tab$std_error[rows]
  names(est) <- model_terms
  names(se) <- model_terms
  ord <- order(est)

  png(file, width = 950, height = 650, res = 130)
  op <- par(mar = c(5, 9, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  y <- barplot(
    est[ord],
    horiz = TRUE,
    names.arg = unname(display_names[names(est)[ord]]),
    las = 1,
    col = "#1f3a5f",
    border = NA,
    xlim = c(min(est - 2 * se), 1),
    xlab = "effect on average finishing position (vs. baseline teams)",
    main = paste(
      "Team effect, 2022 season",
      "(negative = better average finishing position)",
      sep = "\n"
    )
  )

  arrows(
    est[ord] - 1.96 * se[ord], y,
    est[ord] + 1.96 * se[ord], y,
    angle = 90,
    code = 3,
    length = 0.05,
    col = "black"
  )
  abline(v = 0, lty = 2, col = "gray40")

  invisible(file)
}
