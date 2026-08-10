---
layout: ../../../layouts/ProjectOverview.astro
title: "Who’s actually the best F1 driver?"
eyebrow: Statistical modelling
lead: Companion code and technical walkthrough for our joint paper on separating driver performance from car advantage with time–rank duality.
author: Silvio Fanzon
published: Mar. 18, 2024
resources:
  - label: Paper PDF
    href: https://www.silviofanzon.com/assets/pdf/journal/2024-Fry-Bri-Fan.pdf
  - label: Journal article
    href: https://doi.org/10.1016/j.econlet.2024.111671
  - label: GitHub
    href: https://github.com/sfanzon/F1-Paper-Code
glance:
  - label: Question
    text: How much of a race result comes from the driver, and how much from the car?
  - label: Model
    text: Connect a tractable race-time model to observable finishing ranks, then use separate datasets to benchmark constructor effects and compare drivers with their cars.
  - label: Finding
    text: Constructor quality is the dominant source of variation; the driver comparison then identifies expected performances that beat the benchmark implied by the car.
views:
  - number: '01'
    title: Project overview
    description: The question, evidence and result
    href: /projects/f1-time-rank-duality/
  - number: '02'
    title: Technical walkthrough
    description: Paper and R code, step by step
    href: https://www.silviofanzon.com/projects/f1-time-rank-duality/technical.html
  - number: '03'
    title: Code & data
    description: R scripts, data and reproducibility files
    href: https://www.silviofanzon.com/projects/f1-time-rank-duality/code.html
---

<aside class="project-role-note">
This project presents joint work with John Fry and Tom Brighton. I am a co-author of the paper and developed this website account around a checked, reproducible implementation of the published analysis.
</aside>

<aside class="headline-box">
<strong>The headline result:</strong> the analysis learns a conservative teammate-gap threshold from the 2022 season, then applies it to expected positions inferred from the 2023 Qatar Grand Prix odds. <strong>Max Verstappen</strong> and <strong>Fernando Alonso</strong> are the only drivers whose within-team gaps exceed that threshold.
</aside>

## The problem

When Max Verstappen wins a race, how much of that is Max — and how much is the Red Bull?

This is a hard identification problem. Driver and car are tightly confounded because a driver only competes in their own team’s machinery. Earlier econometric studies often pool many seasons and exploit drivers changing teams. That is valuable historically, but it is less helpful when the question is: **who is outperforming their car now?**

Our paper shows how to reach an informative comparison using **one season of public race results and the betting odds for one later race**. The key is a bridge between two ways of modelling the same race.

## Two models, one bridge

**The time model.** Treat each car’s finishing time as exponentially distributed, $T_i \sim \mathrm{Exp}(\lambda_i)$. Larger $\lambda_i$ means a faster latent race time. The resulting win probability is exactly

$$
\Pr(\text{car }j\text{ wins})=
\frac{\lambda_j}{\lambda_1+\cdots+\lambda_n}.
$$

This is mathematically clean and easy to calibrate to bookmaker probabilities, but complete finishing times are usually unavailable because lapped cars do not cover the full race distance.

**The rank model.** Finishing positions are public, so model each rank as Gaussian, $r_i\sim N(\mu_i,\sigma^2)$. The model again gives a closed-form win probability.

**Time–rank duality.** Equating the two win probabilities translates the bookmaker information from the time model into expected finishing positions in the rank model. The analysis gets the tractability of the first model and the observability of the second.

### How the analysis works

<p class="analysis-pipeline-intro">This is the modelling pipeline, not page navigation. The first two stages translate market information into expected ranks; the final two learn and apply a historical benchmark.</p>

<div class="analysis-pipeline" aria-label="Four stages of the Formula 1 analysis">
  <div><span>Input</span><strong>2023 race odds</strong><small>Convert bookmaker odds into adjusted win probabilities.</small></div>
  <div><span>Translation</span><strong>Time–rank duality</strong><small>Turn those probabilities into expected finishing positions.</small></div>
  <div><span>Benchmark</span><strong>2022 season model</strong><small>Estimate constructor effects and a conservative teammate threshold.</small></div>
  <div><span>Decision</span><strong>Teammate comparison</strong><small>Flag expected-rank gaps that exceed the car-only benchmark.</small></div>
</div>

<aside class="project-callout">
<strong>Two datasets have different jobs.</strong> The 2022 results estimate the historical benchmark. The 2023 Qatar odds produce the expected ranks to which that benchmark is applied. Keeping those stages separate is essential.
</aside>

## First look: cars dominate the raw results

The first picture is deliberately descriptive. Each point is a driver’s average finishing position over the 25 recorded races and sprints in 2022, with teammates placed side by side.

<figure>
  <img src="https://www.silviofanzon.com/projects/f1-time-rank-duality/figures/03_driver_vs_team.png" alt="Each Formula 1 driver's average 2022 finishing position, grouped by constructor with teammates side by side." loading="lazy" />
  <figcaption>Each driver’s observed average finishing position in 2022, grouped by constructor. Lower positions are better.</figcaption>
</figure>

<details class="project-code-disclosure">
  <summary>Show the base-R code for this figure</summary>
  <pre><code>#' Figure 3: each driver's observed 2022 average, grouped by constructor
#'
#' This is a descriptive plot of the historical dataset. It is useful for
#' seeing the large constructor differences and the within-team spreads, but
#' it is not the Section 5 driver-versus-car calculation. Section 5 uses the
#' 2023 odds-implied expected ranks shown in Figure 4.
#'
#' @param driver_table output from driver_average_table()
#' @param file output PNG path
plot_driver_vs_team &lt;- function(
    driver_table,
    file = "figures/03_driver_vs_team.png"
) {
  team_order &lt;- c(
    "RedBull", "Mercedes", "Ferrari", "McLaren", "Alpine",
    "AstonMartin", "Haas", "AlphaTauri", "AlfaRomeo", "Williams"
  )
  axis_labels &lt;- c(
    "RedBull", "Mercedes", "Ferrari", "Mclaren", "Alpine",
    "AstonMartin", "Haas", "AlfaTauri", "AlfaRomeo", "Williams"
  )

  dt &lt;- driver_table
  dt&#36;constructor &lt;- factor(dt&#36;constructor, levels = team_order)
  dt &lt;- dt[order(dt&#36;constructor, dt&#36;second_driver), , drop = FALSE]

  teammate_number &lt;- ave(
    seq_len(nrow(dt)),
    dt&#36;constructor,
    FUN = seq_along
  )
  x &lt;- as.numeric(dt&#36;constructor) + ifelse(teammate_number == 1, -0.15, 0.15)
  last_name &lt;- sub("([A-Z][a-z]+)([A-Z].*)", "\\2", dt&#36;driver)

  # Small label adjustments keep neighbouring names readable while preserving
  # the original plot's side-by-side structure.
  y_shift &lt;- rep(0.48, nrow(dt))
  y_shift[last_name %in% c("Russel", "Leclerc", "Bottas")] &lt;- -0.48
  y_shift[last_name %in% c("Magnussen", "Schumacher", "Tsunoda", "Guanyu")] &lt;- 0.62

  png(file, width = 1000, height = 680, res = 130)
  op &lt;- par(mar = c(7, 5, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  plot(
    x,
    dt&#36;avg_position,
    pch = 19,
    col = "#cc0164",
    cex = 1.3,
    xaxt = "n",
    xlab = "",
    ylab = "average finishing position (2022 season)",
    xlim = c(min(x) - 0.4, max(x) + 0.3),
    ylim = c(min(dt&#36;avg_position) - 0.8, max(dt&#36;avg_position) + 1.3),
    main = paste(
      "Each driver's actual average position, by team",
      "(teammates plotted side by side)",
      sep = "\\n"
    )
  )

  axis(1, at = seq_along(team_order), labels = axis_labels, las = 2)
  for (i in seq_along(team_order)) {
    abline(v = i, col = "gray90", lty = 3)
  }
  points(x, dt&#36;avg_position, pch = 19, col = "#cc0164", cex = 1.3)
  text(
    x,
    dt&#36;avg_position + y_shift,
    labels = last_name,
    cex = 0.65
  )

  invisible(file)
}</code></pre>
</details>

The large jumps between constructors show immediately why car quality cannot be ignored. Red Bull, Mercedes and Ferrari occupy a very different part of the plot from the back of the grid. The smaller gaps within each constructor suggest an additional driver-level effect — but these raw averages are **not** the final comparison.

## Estimate the car effect rather than eyeballing it

The regression uses all 500 driver-race observations. It explains finishing position using constructor indicators while retaining a second-driver indicator. The constructor coefficients below are relative to the omitted baseline teams; negative values mean a better expected finishing position.

<figure>
  <img src="https://www.silviofanzon.com/projects/f1-time-rank-duality/figures/02_team_effects.png" alt="Constructor coefficients from the 2022 Formula 1 regression with confidence intervals." loading="lazy" />
  <figcaption>Estimated constructor effects from the selected 2022 regression, with 95% confidence intervals.</figcaption>
</figure>

<details class="project-code-disclosure">
  <summary>Show the base-R code for this figure</summary>
  <pre><code>#' Figure 2: constructor effects from the selected 2022 regression
#'
#' @param model fitted model returned by select_models()&#36;stepwise
#' @param file output PNG path
plot_team_effects &lt;- function(
    model,
    file = "figures/02_team_effects.png"
) {
  tab &lt;- regression_table(model)
  model_terms &lt;- c(
    "RedBull", "Mercedes", "Ferrari", "McLaren", "Alpine", "AstonMartin"
  )
  display_names &lt;- c(
    RedBull = "RedBull",
    Mercedes = "Mercedes",
    Ferrari = "Ferrari",
    McLaren = "Mclaren",
    Alpine = "Alpine",
    AstonMartin = "AstonMartin"
  )

  rows &lt;- match(model_terms, tab&#36;term)
  est &lt;- tab&#36;estimate[rows]
  se &lt;- tab&#36;std_error[rows]
  names(est) &lt;- model_terms
  names(se) &lt;- model_terms
  ord &lt;- order(est)

  png(file, width = 950, height = 650, res = 130)
  op &lt;- par(mar = c(5, 9, 3, 1))
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  y &lt;- barplot(
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
      sep = "\\n"
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
}</code></pre>
</details>

The ordering matches the intuitive picture, but the model makes the comparison explicit. Red Bull has the largest estimated advantage, followed by Mercedes and Ferrari. The estimated second-driver penalty is only $0.216$ positions and is statistically uncertain; its 95% confidence interval is $(-0.581,\ 1.013)$.

The upper endpoint, **1.013 positions**, becomes a conservative benchmark. A later within-team expected-rank gap above this value is larger than the historical car-and-teammate pattern can comfortably explain.

## Apply the benchmark to the 2023 Qatar odds

Bookmaker odds for the Qatar Grand Prix are converted into implied win probabilities, adjusted for the bookmaker margin, and translated through the duality into expected finishing ranks. The analysis then compares the two expected ranks within each constructor.

<figure>
  <img src="https://www.silviofanzon.com/projects/f1-time-rank-duality/figures/04_teammate_gaps.png" alt="Odds-implied Formula 1 teammate gaps, with Verstappen and Alonso above the historical threshold." loading="lazy" />
  <figcaption>Odds-implied teammate gaps for the 2023 Qatar Grand Prix. The dashed line is the 1.013-position historical threshold.</figcaption>
</figure>

<details class="project-code-disclosure">
  <summary>Show the base-R code for this figure</summary>
  <pre><code>#' Figure 4: odds-implied teammate gaps compared with the historical threshold
#'
#' @param gaps output from teammate_gaps()
#' @param threshold upper endpoint from second_driver_ci()
#' @param file output PNG path
plot_teammate_gaps &lt;- function(
    gaps,
    threshold,
    file = "figures/04_teammate_gaps.png"
) {
  gaps &lt;- gaps[order(-gaps&#36;gap), , drop = FALSE]
  labels &lt;- paste0(gaps&#36;leading_driver, "  (", gaps&#36;team, ")")
  cols &lt;- ifelse(gaps&#36;outperforms_car, "#C8102E", "grey65")

  png(file, width = 1800, height = 1050, res = 180)
  op &lt;- par(mar = c(5, 15, 3, 2), xpd = NA)
  on.exit({
    par(op)
    dev.off()
  }, add = TRUE)

  bp &lt;- barplot(
    rev(gaps&#36;gap),
    horiz = TRUE,
    col = rev(cols),
    border = NA,
    names.arg = rev(labels),
    las = 1,
    cex.names = 0.78,
    xlim = c(0, max(gaps&#36;gap) * 1.08),
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
}</code></pre>
</details>

Two drivers — and only two — clear the threshold:

- **Max Verstappen versus Sergio Perez:** an expected-position gap of about **7.669**;
- **Fernando Alonso versus Lance Stroll:** an expected-position gap of about **2.403**.

The remaining within-team gaps are below 1.013. In the language of the model, Verstappen and Alonso are the two drivers whose market-implied advantage over their teammates is too large to attribute to the car-only benchmark learned from 2022.

<aside class="project-callout important">
<strong>What this does not say:</strong> the raw 2022 teammate averages are not tested against the threshold. They are useful context, while the final comparison uses the <strong>2023 odds-implied expected ranks</strong>. The <a href="https://www.silviofanzon.com/projects/f1-time-rank-duality/technical.html">technical walkthrough</a> documents the distinction and reproduces the relevant tables and checks.
</aside>

## From a paper to a reproducible analysis

The implementation is part of the project, not an afterthought. The updated repository contains:

- two explicit input datasets rather than hidden or hard-coded values;
- small base-R modules for odds calibration, rank duality, regression and driver effects;
- a one-command script reproducing Tables 1–3 and the final comparison;
- tests against the paper’s published values;
- four figures generated directly in R, with the exact plotting code shown beside the explanation.

This separation matters in applied work: the descriptive plot, the fitted model and the final decision rule each answer a different question, and the code keeps those stages auditable.

## Responsible interpretation

“Outperforming the car” is a model-based statement, not a direct measurement of immutable driver ability. It combines a threshold estimated from 2022 with information embedded in one race’s 2023 betting market. The conclusion depends on assumptions including independent exponential race times, a Gaussian rank approximation, common rank variance and the information contained in bookmaker odds.

The strength of the project is not that those assumptions are invisible; it is that the full chain from data to claim is explicit, reproducible and open to scrutiny.

## Why I like this project

1. **Tractability becomes useful information.** Choosing models with exact win probabilities makes the time–rank bridge possible.
2. **Constraints reduce the data burden.** The fact that ranks always sum to $n(n+1)/2$ identifies a parameter that would otherwise need estimating.
3. **A sharp question beats brute force.** Careful structure extracts a current-season comparison from far less historical data than a large pooled model.

The method extends beyond motorsport to any setting where you observe *rankings* but reason about *latent performance* — horse racing, esports, even recruitment funnels.

## Citation and licence

If the paper or companion code is useful in your work, please cite the published article [Faster identification of faster Formula 1 drivers via time–rank duality](https://doi.org/10.1016/j.econlet.2024.111671). The maintained code is available at [sfanzon/F1-Paper-Code](https://github.com/sfanzon/F1-Paper-Code). Code and data are released under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

```bibtex
@article{2024-Fry-Bri-Fan,
  author  = {Fry, John and Brighton, Tom and Fanzon, Silvio},
  title   = {Faster identification of faster Formula 1 drivers via time-rank duality},
  journal = {Economics Letters},
  volume  = {237},
  pages   = {111671},
  year    = {2024},
  doi     = {10.1016/j.econlet.2024.111671}
}
```
