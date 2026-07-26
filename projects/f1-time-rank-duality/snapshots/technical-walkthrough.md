::: {.headline-box}
This walkthrough reproduces Tables 1–3 and Section 5 of the published analysis with two distinct data
sources [@fry2024f1]. The corrected Section 5 calculation compares **Table 2's 2023
odds-implied expected ranks** within each team; it does not compare raw 2022
season averages.
:::

For a shorter, industry-facing account, read the [project overview](index.qmd).
The complete pipeline is run with:

```bash
Rscript analysis/reproduce_paper.R
Rscript tests/run_tests.R
```

To regenerate only the figures:

```bash
Rscript analysis/generate_figures.R
```

No external R packages are required. All four committed figures are generated
with base R; none is manually drawn or produced in Python. The exact plotting
source is shown below each figure in a collapsed block and lives under
`R/figures/`.

## Reproducibility map {data-nav-title="Reproducibility"}

| Paper component | Input | Implementation |
|---|---|---|
| Table 1 | 2023 Qatar bookmaker odds | `R/00_utils.R`, `R/01_odds_calibration.R` |
| Table 2 | Table 1 win probabilities | `R/02_rank_duality.R` |
| Table 3 | 2022 finishing positions | `R/03_regression.R` |
| Section 5 | Table 3 CI + Table 2 expected ranks | `R/04_driver_effects.R` |
| Figures | reproduced model objects | `R/05_visualization.R`, `R/figures/` |

## From bookmaker odds to win probabilities {data-nav-title="Bookmaker odds"}

For fractional odds $a/b$, the raw implied probability is

$$p_{\mathrm{raw}}=\frac{b}{a+b}.$$

The raw probabilities include the bookmaker's overround, so they are divided
by their sum [@strumbelj2014betting]. The Qatar odds are stored as data rather than hard-coded inside
an objective function.

```r
odds_to_probs <- function(odds) {
  fractional <- parse_fractional_odds(odds)
  raw <- 1 / (fractional + 1)
  raw / sum(raw)
}

odds <- read_qatar_odds("data/qatar2023_odds.csv")
```

The recomputed probabilities agree with the values printed in Table 1 up to
the rounding of the published table.

## Exponential race-time calibration {data-nav-title="Race-time calibration"}

Assume independent finishing times

$$T_i\sim\operatorname{Exp}(\lambda_i).$$

Then

$$
\Pr(\text{car }i\text{ wins})=
\frac{\lambda_i}{\sum_j\lambda_j}.
$$

The paper proposes minimising

$$
\operatorname{RSS}(\lambda)=
\sum_i\left(\frac{\lambda_i}{\sum_j\lambda_j}-p_i\right)^2.
$$

### The scale is not identifiable

The objective only uses normalised rates. Therefore, for every $c>0$,

$$\lambda_i=c\,p_i$$

has zero RSS. The absolute scale of Table 1 is not estimated by the win
probabilities; only the ratios are identified.

The corrected code makes the exact solution the primary implementation:

```r
lambda_from_probs <- function(probs, scale = 1) {
  assert_probabilities(probs)
  scale * probs
}
```

It also retains a numerical check, but removes the degeneracy by normalising
inside the objective and enforces positivity through log-rates:

```r
numerical <- estimate_lambda_numerically(
  odds$implied_probability,
  restarts = 20,
  seed = 1
)
```

The unit-sum numerical rates agree with `lambda = p`. To compare with Table 1,
the code estimates the common multiplier that best maps the rounded published
probabilities to the rounded published lambda column.

![](figures/01_lambda_estimates.png){width="92%" fig-align="center" fig-alt="Estimated exponential race-time rate for each driver from Qatar 2023 bookmaker odds."}

::: {.callout-note collapse="true" appearance="minimal" title="Show the R code for Figure 1"}

```r
#' Figure 1: odds-implied exponential rates
#'
#' @param calibration output from build_calibration_table()
#' @param file output PNG path
plot_lambda_estimates <- function(
    calibration,
    file = "figures/01_lambda_estimates.png"
) {
  ord <- order(-calibration$lambda_paper_scale)
  driver_labels <- sub("^.* ", "", calibration$driver)

  png(file, width = 900, height = 650, res = 130, bg = sf_color("paper"))
  op <- sf_plot_par(c(7, 5, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  barplot(
    calibration$lambda_paper_scale[ord],
    names.arg = driver_labels[ord],
    las = 2,
    col = sf_color("blue"),
    border = NA,
    ylab = expression(hat(lambda)),
    main = paste(
      "Estimated race-time rate per driver",
      "(2023 Qatar GP bookmakers' odds, exponential model)",
      sep = "
"
    )
  )
  abline(h = 0, col = sf_color("sand"))

  invisible(file)
}
```
:::

::: {.callout-important}
The bar heights use the paper's common scale for visual comparability. A
rescaling changes the axis values but not a single predicted win probability or
substantive conclusion.
:::

## Time-rank duality and Table 2 {data-nav-title="Time-rank duality"}

The rank model approximates final rank by

$$r_i\sim N(\mu_i,\sigma^2).$$

Using the continuity-corrected event $r_i\le 1.5$,

$$p_i=\Phi\left(\frac{1.5-\mu_i}{\sigma}\right),$$

so

$$\mu_i=1.5-\sigma\Phi^{-1}(p_i).$$

Because ranks sum to $n(n+1)/2$, the common standard deviation is

$$
\sigma=
\frac{n-n^2/2}{\sum_i\Phi^{-1}(p_i)}.
$$

```r
implied_rank_params <- function(probs) {
  n <- length(probs)
  z <- qnorm(probs)
  sigma <- (n - n^2 / 2) / sum(z)
  mu <- 1.5 - sigma * z
  list(mu = mu, sigma = sigma)
}
```

The reproduction gives

```text
sigma_hat = 3.879374
mu_hat(Max Verstappen) = -0.242969
mu_hat(Fernando Alonso) = 10.501519
```

matching Table 2.

## Historical regression and Table 3 {data-nav-title="Historical regression"}

The second dataset contains 20 drivers over 25 events in 2022. This follows the paper’s one-season strategy rather than pooling many decades of Formula One history [@fry2024f1]. It is reshaped
to one row per driver-event. The candidate model is

$$
\text{position}
\sim \text{second driver} + \text{constructor indicators},
$$

with Williams as the omitted baseline. Every candidate model is constrained to
keep the second-driver term.

```r
f1 <- load_f1_2022("data/f1_2022_positions.txt")
models <- select_models(f1)
summary(models$stepwise)
```

The selected model reproduces Table 3:

```text
                    Estimate  Std. Error  t value
(Intercept)          13.8420      0.3794   36.484
second_driver         0.2160      0.4056    0.533
RedBull               -9.6500      0.7170  -13.459
Mercedes              -8.2700      0.7170  -11.534
Ferrari               -7.6900      0.7170  -10.725
McLaren               -3.5500      0.7170   -4.951
Alpine                -3.5500      0.7170   -4.951
AstonMartin           -1.7900      0.7170   -2.496

R-squared = 0.3914
```

Forward and both-direction selection return the same smaller model. Backward
selection retains three additional constructor terms, but the nested-model
F-test has $p\approx0.079$, so the paper retains the smaller model.

![](figures/02_team_effects.png){width="92%" fig-align="center" fig-alt="Constructor coefficients from the selected 2022 regression, with confidence intervals."}

The bars are the constructor coefficients relative to Williams, the omitted
baseline. A negative coefficient means a better expected finishing position.
The error bars are 95% intervals based on the fitted linear model.

::: {.callout-note collapse="true" appearance="minimal" title="Show the R code for Figure 2"}

```r
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
    RedBull = "Red Bull",
    Mercedes = "Mercedes",
    Ferrari = "Ferrari",
    McLaren = "McLaren",
    Alpine = "Alpine",
    AstonMartin = "Aston Martin"
  )

  rows <- match(model_terms, tab$term)
  est <- tab$estimate[rows]
  se <- tab$std_error[rows]
  names(est) <- model_terms
  names(se) <- model_terms
  ord <- order(est)

  png(file, width = 950, height = 650, res = 130, bg = sf_color("paper"))
  op <- sf_plot_par(c(5, 9, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  y <- barplot(
    est[ord],
    horiz = TRUE,
    names.arg = unname(display_names[names(est)[ord]]),
    las = 1,
    col = sf_color("blue"),
    border = NA,
    xlim = c(min(est - 2 * se), 1),
    xlab = "effect on average finishing position (vs. baseline teams)",
    main = paste(
      "Team effect, 2022 season",
      "(negative = better average finishing position)",
      sep = "
"
    )
  )

  arrows(
    est[ord] - 1.96 * se[ord], y,
    est[ord] + 1.96 * se[ord], y,
    angle = 90,
    code = 3,
    length = 0.05,
    col = sf_color("ink")
  )
  abline(v = 0, lty = 2, lwd = 1.4, col = sf_color("gold"))

  invisible(file)
}
```
:::

### A descriptive check: raw driver averages by constructor

The next figure summarises the same 2022 data before regression. For each
driver, it averages the 25 observed finishing positions and places teammates
side by side.

![](figures/03_driver_vs_team.png){width="100%" fig-align="center" fig-alt="Each driver's average 2022 finishing position, grouped by constructor."}

The plot makes two features visible. First, the large differences across
constructors confirm that car quality is the dominant source of variation.
Second, the two points within a team are not identical, which motivates the
second-driver term. However, these raw means are not adjusted model effects and
are **not** the quantities used for the paper's final 2023 driver comparison.

The implementation calculates the averages from the long-form data rather than
hard-coding the plotted values:

```r
driver_averages <- driver_average_table(f1)
```

::: {.callout-note collapse="true" appearance="minimal" title="Show the R code for Figure 3"}

```r
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
    "Red Bull", "Mercedes", "Ferrari", "McLaren", "Alpine",
    "Aston Martin", "Haas", "AlphaTauri", "Alfa Romeo", "Williams"
  )

  dt <- driver_table
  dt$constructor <- factor(dt$constructor, levels = team_order)
  dt <- dt[order(dt$constructor, dt$second_driver), , drop = FALSE]

  teammate_number <- ave(seq_len(nrow(dt)), dt$constructor, FUN = seq_along)
  x <- as.numeric(dt$constructor) + ifelse(teammate_number == 1, -0.15, 0.15)
  last_name <- sub("([A-Z][a-z]+)([A-Z].*)", "\2", dt$driver)

  y_shift <- rep(0.48, nrow(dt))
  y_shift[last_name %in% c("Russel", "Leclerc", "Bottas")] <- -0.48
  y_shift[last_name %in% c("Magnussen", "Schumacher", "Tsunoda", "Guanyu")] <- 0.62

  png(file, width = 1000, height = 680, res = 130, bg = sf_color("paper"))
  op <- sf_plot_par(c(7, 5, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  plot(
    x,
    dt$avg_position,
    pch = 19,
    col = sf_color("rust"),
    cex = 1.3,
    xaxt = "n",
    xlab = "",
    ylab = "average finishing position (2022 season)",
    xlim = c(min(x) - 0.4, max(x) + 0.3),
    ylim = c(min(dt$avg_position) - 0.8, max(dt$avg_position) + 1.3),
    main = paste(
      "Each driver's actual average position, by team",
      "(teammates plotted side by side)",
      sep = "
"
    )
  )

  axis(1, at = seq_along(team_order), labels = axis_labels, las = 2)
  for (i in seq_along(team_order)) {
    abline(v = i, col = sf_color("sand"), lty = 3)
  }
  points(x, dt$avg_position, pch = 19, col = sf_color("rust"), cex = 1.3)
  text(x, dt$avg_position + y_shift, labels = last_name, cex = 0.65,
       col = sf_color("ink"))

  invisible(file)
}
```
:::

## The correct driver-level comparison {data-nav-title="Driver comparison"}

The second-driver coefficient has the 95% confidence interval

$$(-0.581,\ 1.013).$$

The upper endpoint is used as the threshold. The next step is often easy to
misread: the paper compares the **odds-implied expected ranks from Table 2**
within each 2023 constructor.

```r
ci <- second_driver_ci(models$stepwise)
dual <- implied_rank_params(odds$implied_probability)
gaps <- teammate_gaps(odds, dual$mu, threshold = ci["upper"])
```

Selected output:

```text
team          leading driver       teammate          gap    exceeds 1.013
Red Bull      Max Verstappen       Sergio Perez      7.669  yes
Aston Martin  Fernando Alonso      Lance Stroll      2.403  yes
McLaren       Lando Norris         Oscar Piastri     0.515  no
Ferrari       Charles Leclerc      Carlos Sainz      0.187  no
```

![](figures/04_teammate_gaps.png){width="100%" fig-align="center" fig-alt="Odds-implied teammate gaps for Qatar 2023 with the historical threshold marked."}

The dashed line is the upper confidence limit from the 2022 second-driver
coefficient. The rust-coloured bars are the only 2023 within-team expected-rank gaps that
exceed it.

::: {.callout-note collapse="true" appearance="minimal" title="Show the R code for Figure 4"}

```r
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
  cols <- ifelse(gaps$outperforms_car, sf_color("rust"), sf_color("slate_light"))

  png(file, width = 1800, height = 1050, res = 180, bg = sf_color("paper"))
  op <- sf_plot_par(c(5, 15, 3, 2))
  par(xpd = NA)
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

  abline(v = threshold, lty = 2, lwd = 2, col = sf_color("gold"))
  text(
    threshold,
    max(bp),
    pos = 4,
    cex = 0.8,
    col = sf_color("gold"),
    labels = sprintf("car-only threshold = %.3f", threshold)
  )

  invisible(file)
}
```
:::

::: {.callout-important}
### Why the previous dual-page version produced a contradiction

It applied the threshold to raw 2022 teammate average positions. That is a
different calculation from Section 5 and mixes the 2022 grid with a conclusion
based on the 2023 Qatar field. In particular, Alonso drove for Alpine in 2022
but appears for Aston Martin in the 2023 odds. The corrected pipeline keeps
those roles and seasons separate.
:::

## Validation and limitations {data-nav-title="Validation"}

`tests/run_tests.R` checks the published probability column, Table 1 scaled
rates, Table 2 values, Table 3 coefficients and $R^2$, the confidence interval,
the descriptive driver averages, and the final pair of flagged drivers.

The reproduction validates the arithmetic and code path; it does not remove
the modelling assumptions. In particular:

- finishing times are assumed independent in the exponential model;
- ranks use a Gaussian approximation and a common variance;
- bookmaker odds contain market information and are not a pure skill measure;
- stepwise model selection can be unstable and should be interpreted as part
  of the paper's specified procedure, not as a universally preferred method;
- retirements and incomplete race distances are not explicitly modelled.

## Files produced {data-nav-title="Outputs"}

```text
output/table1_calibration.csv
output/table2_rank_parameters.csv
output/table3_regression.csv
output/driver_average_positions.csv
output/section5_teammate_gaps.csv
figures/01_lambda_estimates.png
figures/02_team_effects.png
figures/03_driver_vs_team.png
figures/04_teammate_gaps.png
```

The [published paper](https://www.silviofanzon.com/assets/pdf/journal/2024-Fry-Bri-Fan.pdf)
contains the theoretical development and complete discussion.
