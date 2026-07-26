#' Figure 3: each driver's observed 2022 average, grouped by constructor
#'
#' This is a descriptive plot of the historical dataset. It is useful for
#' seeing the large constructor differences and the within-team spreads, but
#' it is not the Section 5 driver-versus-car calculation. Section 5 uses the
#' 2023 odds-implied expected ranks shown in Figure 4.
#'
#' @param driver_table output from driver_average_table()
#' @param file output PNG path
plot_driver_vs_team <- function(
    driver_table,
    file = "figures/03_driver_vs_team.png"
) {
  team_order <- c(
    "RedBull", "Mercedes", "Ferrari", "McLaren", "Alpine",
    "AstonMartin", "Haas", "AlphaTauri", "AlfaRomeo", "Williams"
  )
  axis_labels <- c(
    "RedBull", "Mercedes", "Ferrari", "Mclaren", "Alpine",
    "AstonMartin", "Haas", "AlfaTauri", "AlfaRomeo", "Williams"
  )

  dt <- driver_table
  dt$constructor <- factor(dt$constructor, levels = team_order)
  dt <- dt[order(dt$constructor, dt$second_driver), , drop = FALSE]

  teammate_number <- ave(
    seq_len(nrow(dt)),
    dt$constructor,
    FUN = seq_along
  )
  x <- as.numeric(dt$constructor) + ifelse(teammate_number == 1, -0.15, 0.15)
  last_name <- sub("([A-Z][a-z]+)([A-Z].*)", "\\2", dt$driver)

  # Small label adjustments keep neighbouring names readable while preserving
  # the original plot's side-by-side structure.
  y_shift <- rep(0.48, nrow(dt))
  y_shift[last_name %in% c("Russel", "Leclerc", "Bottas")] <- -0.48
  y_shift[last_name %in% c("Magnussen", "Schumacher", "Tsunoda", "Guanyu")] <- 0.62

  png(file, width = 1000, height = 680, res = 130)
  op <- par(mar = c(7, 5, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  plot(
    x,
    dt$avg_position,
    pch = 19,
    col = "#cc0164",
    cex = 1.3,
    xaxt = "n",
    xlab = "",
    ylab = "average finishing position (2022 season)",
    xlim = c(min(x) - 0.4, max(x) + 0.3),
    ylim = c(min(dt$avg_position) - 0.8, max(dt$avg_position) + 1.3),
    main = paste(
      "Each driver's actual average position, by team",
      "(teammates plotted side by side)",
      sep = "\n"
    )
  )

  axis(1, at = seq_along(team_order), labels = axis_labels, las = 2)
  for (i in seq_along(team_order)) {
    abline(v = i, col = "gray90", lty = 3)
  }
  points(x, dt$avg_position, pch = 19, col = "#cc0164", cex = 1.3)
  text(
    x,
    dt$avg_position + y_shift,
    labels = last_name,
    cex = 0.65
  )

  invisible(file)
}
