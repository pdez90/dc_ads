# Selling the Cloud — an archive of data center ads and their energy & water claims
# Deploy: Posit Connect Cloud -> New content -> Shiny -> point at this folder (app.R + data/)
library(shiny)
library(bslib)
library(DT)
library(htmltools)
library(wordcloud)

rd <- function(f) {
  p <- file.path("data", f)
  h <- strsplit(readLines(p, n = 1, encoding = "UTF-8", warn = FALSE), ",")[[1]]
  cc <- c(library_id = "character", uid = "character")
  read.csv(p, stringsAsFactors = FALSE, na.strings = "", encoding = "UTF-8", colClasses = cc[names(cc) %in% h])
}
campaigns <- rd("campaigns.csv")
videos    <- rd("youtube_ads.csv")
meta_ads  <- rd("meta_ads.csv")
meta_n    <- rd("meta_counts.csv")
lawsuits  <- rd("lawsuits.csv")
template  <- rd("template_by_state.csv")
ads       <- rd("ads_all.csv")
wf        <- rd("word_freq.csv")
maud      <- rd("meta_audience.csv")

esc  <- function(x) htmlEscape(ifelse(is.na(x), "", x))
nz   <- function(x) ifelse(is.na(x), "", x)
link <- function(url, label) ifelse(is.na(url) | url == "", "",
                                    sprintf('<a href="%s" target="_blank" rel="noopener">%s</a>', esc(url), label))
claim_class <- function(ct) {
  ct <- tolower(ifelse(is.na(ct), "", ct))
  ifelse(grepl("counter", ct), "counter",
  ifelse(grepl("energy", ct) & grepl("water", ct), "both",
  ifelse(grepl("water", ct), "water", ifelse(grepl("energy", ct), "energy", "other"))))
}
FC_LEVELS <- c("Disputed", "Missing context", "Supported", "No public data", "Not yet checked", "Not checkable",
               "No energy/water claim", "Counter-ad (not rated)")
fc_class <- function(x) c(Disputed = "fc-dis", `Missing context` = "fc-mis", Supported = "fc-sup", `No public data` = "fc-nod",
                          `Not yet checked` = "fc-nod", `Not checkable` = "fc-nc")[nz(x)]
fc_chip <- function(r, note = NULL, url = NULL) {
  cl <- fc_class(r); cl[is.na(cl)] <- "fc-na"
  out <- sprintf('<span class="fc-chip %s">%s</span>', cl, esc(r))
  if (!is.null(note)) out <- paste0(out, ifelse(is.na(note) | note == "", "", paste0('<br><small class="text-muted">', esc(note), "</small>")))
  if (!is.null(url))  out <- paste0(out, ifelse(is.na(url) | url == "", "", paste0(" <small>", link(url, "source ↗"), "</small>")))
  out
}
law_chip <- function(ids, role) ifelse(is.na(ids) | ids == "", "",
  sprintf('<span class="law-chip">⚖ %s</span><br><small>%s</small>', esc(ids), esc(role)))

# "Who sees it": a coarse place + an age profile (Meta only)
STATES <- state.name
area_of <- function(x) {
  x <- nz(x)
  vapply(x, function(s) {
    s2 <- gsub("Washington DC", "", gsub("West Virginia", "WV", s))
    pos <- vapply(STATES, function(st) { m <- regexpr(paste0("\\b", st, "\\b"), s2); as.integer(m) }, integer(1))
    hit <- STATES[pos > 0][order(pos[pos > 0])]
    if (grepl("capitals", s)) "Several states"
    else if (length(hit) > 1 && !grepl("%", s)) "Several states"
    else if (length(hit)) hit[1] else if (grepl("Northern Virginia|Fredericksburg", s)) "Virginia"
    else if (grepl("India|Hyderabad|Chennai|Mumbai|Noida|Nagpur|Visakhapatnam", s)) "India"
    else if (grepl("Chile|UK|London|Korea", s)) "Outside US"
    else if (grepl("NM|Los Lunas", s)) "New Mexico" else if (grepl(", WI", s)) "Wisconsin"
    else if (grepl("Phoenix|AZ", s)) "Arizona" else if (grepl("Memphis", s)) "Tennessee"
    else if (grepl("PA / OH|Pennsylvania, Ohio", s)) "Several states" else "National / other"
  }, character(1), USE.NAMES = FALSE)
}
age_profile <- function(y, o) ifelse(is.na(o), "Not published",
  ifelse(o >= 50, "Mostly 55+", ifelse(y >= 50, "Mostly under 35", "Mixed ages")))
ads$area <- area_of(ads$audience_where)
ads$age_profile <- age_profile(suppressWarnings(as.numeric(ads$age_18_34)), suppressWarnings(as.numeric(ads$age_55_plus)))
ads$fc_rank <- match(ads$factcheck, FC_LEVELS)

theme <- bs_theme(version = 5, bg = "#f6f3ec", fg = "#1b1b18", primary = "#1f6f9a",
                  base_font = font_google("IBM Plex Sans", local = FALSE), heading_font = font_google("Fraunces", local = FALSE),
                  code_font = font_google("IBM Plex Mono", local = FALSE))

css <- "
.claim-chip,.fc-chip,.law-chip{display:inline-block;padding:1px 9px;border-radius:99px;font-size:.75rem;color:#fff;white-space:nowrap}
.c-energy{background:#c26a00}.c-water{background:#1f6f9a}.c-both{background:#5b4b9a}.c-counter{background:#a3322a}.c-other{background:#8a8577}
.fc-dis{background:#a3322a}.fc-mis{background:#b5651d}.fc-sup{background:#2e7d4f}.fc-nod{background:#6b675e}.fc-nc{background:#9a958a}.fc-na{background:#c9c4b8;color:#1b1b18}
.law-chip{background:#1b1b18}
.stat b{display:block;font:700 2rem Fraunces,serif;line-height:1}.stat span{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:#6b675e}
.lede{max-width:820px;color:#4b4840}
.law-card{border-left:5px solid #a3322a}
.video-wrap{position:relative;padding-top:56.25%}.video-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
table.dataTable td{vertical-align:top}
.scale td{padding:4px 10px;vertical-align:top}
"

stat <- function(n, label) div(class = "stat me-4 mb-2", tags$b(n), tags$span(label))
groups_sorted <- sort(unique(ads$appears_as))

ui <- page_navbar(
  title = "Selling the Cloud", theme = theme, bg = "#1b1b18", inverse = TRUE,
  header = tags$head(tags$style(HTML(css))),

  nav_panel("Claims",
    div(class = "container-xl py-3",
      h2("What data center ads say about energy and water"),
      p(class = "lede", "This archive collects TV spots, YouTube pre-roll, Facebook ads, billboards, print ads and company leave-behinds that make energy or water claims about data centers, starting with the US. Each entry records the name the ad appears under, who actually paid for it, what it claims, whether the claim can be checked, and any lawsuit or investigation it's tied to."),
      div(class = "d-flex flex-wrap my-3",
        stat(nrow(ads), "ad records"), stat(nrow(videos), "YouTube ad videos"),
        stat(length(unique(videos$state[grepl("Connect", videos$channel)])), "America Connects state campaigns"),
        stat(format(sum(videos$views, na.rm = TRUE), big.mark = ","), "YouTube views"),
        stat(sum(ads$factcheck == "Disputed", na.rm = TRUE), "ads with disputed claims"),
        stat(sum(ads$in_lawsuit == "Yes"), "ads tied to a lawsuit")),
      layout_columns(col_widths = c(3, 3, 3, 3),
        selectInput("c_region", "Region", c("All", sort(unique(campaigns$region)))),
        selectInput("c_claim", "Claim type", c("All", "Energy", "Water", "Counter-claims")),
        selectInput("c_stype", "Sponsor type", c("All", sort(unique(campaigns$sponsor_type)))),
        selectInput("c_fc", "Fact-check", c("All", FC_LEVELS))),
      DTOutput("t_campaigns"))),

  nav_panel("Find ads",
    div(class = "container-xl py-3",
      h2("Sort and filter every ad"),
      p(class = "lede", HTML("One row per ad record: campaign entries, YouTube ads and Meta ads together. <b>Appears as</b> is the name viewers see on the ad. <b>Paid for by</b> is who actually funded it, from the ad libraries' disclaimers. <b>Who sees it</b> is where the ad ran and, for Facebook and Instagram issue ads, Meta's age and gender breakdown of who it reached. Click any column header to sort.")),
      layout_columns(col_widths = c(3, 3, 3, 3),
        selectInput("f_law", "Part of a lawsuit?", c("All", "Yes: any lawsuit", "No", setNames(lawsuits$id, paste(lawsuits$id, "–", substr(lawsuits$title, 1, 40))))),
        selectizeInput("f_group", "Appears as (group)", c("All", groups_sorted)),
        selectInput("f_area", "Who sees it: where", c("All", sort(unique(ads$area)))),
        selectInput("f_age", "Who sees it: age (Meta)", c("All", "Mostly 55+", "Mostly under 35", "Mixed ages", "Not published"))),
      layout_columns(col_widths = c(3, 3, 3, 3),
        selectInput("f_kind", "Record type", c("All", sort(unique(ads$kind)))),
        selectInput("f_fc", "Fact-check", c("All", "Checkable claims only", FC_LEVELS)),
        selectInput("f_sort", "Sort by", c("Lawsuit first" = "law", "Group (appears as)" = "group", "Who sees it (place)" = "area",
                                          "Fact-check (most disputed first)" = "fc", "Date (newest first)" = "date")),
        div(class = "pt-4", downloadButton("dl_ads", "Download filtered rows (CSV)", class = "btn-sm"))),
      DTOutput("t_ads"))),

  nav_panel("Word cloud",
    div(class = "container-xl py-3",
      h2("The words the ads use"),
      p(class = "lede", "Word counts from the ad scripts: YouTube auto-captions, Meta ad text and quoted claims for other ads. Common words and the words \"data\" and \"center(s)\" are dropped. Filter to compare groups, or to compare ads tied to lawsuits with the rest."),
      layout_columns(col_widths = c(3, 9),
        card(
          selectizeInput("w_group", "Appears as", c("All", sort(unique(wf$appears_as))), multiple = FALSE),
          selectInput("w_law", "Part of a lawsuit?", c("All", "Yes", "No")),
          selectInput("w_kind", "Record type", c("All", sort(unique(wf$kind)))),
          selectInput("w_fc", "Fact-check", c("All", FC_LEVELS)),
          sliderInput("w_max", "Words shown", 20, 150, 80, step = 10),
          tableOutput("w_top")),
        card(plotOutput("w_cloud", height = "620px"), uiOutput("w_n"))))),

  nav_panel("YouTube ads",
    div(class = "container-xl py-3",
      h2("Data center video ads on YouTube"),
      p(class = "lede", HTML("These are videos that verified Google advertisers ran as ads. <b>America Connects</b>, the Data Center Coalition's state-campaign nonprofit, has about 300 ads, with GMMB, Inc. listed as the payer. <b>Build American AI</b> has 38 ads in Ohio and Kansas. <b>QTS Data Centers</b> (about 95), <b>Compass Datacenters</b> (about 155), <b>Texans for Economic Liberty</b> (21) and separate <b>Texas Connects</b> and <b>Oregon Connects</b> accounts are also verified advertisers. Google itself ran 191 data-center community ads in Sept 2026. Click a row to play the ad. Key claims are short excerpts from YouTube's auto-generated transcripts.")),
      layout_columns(col_widths = c(3, 3, 3, 3),
        selectInput("v_state", "State", c("All", sort(unique(videos$state)))),
        selectInput("v_topic", "Topic", c("All", sort(unique(videos$topic)))),
        selectInput("v_group", "Appears as", c("All", sort(unique(videos$appears_as)))),
        checkboxInput("v_trans", "Only transcribed", FALSE)),
      layout_columns(col_widths = c(7, 5),
        DTOutput("t_videos"),
        card(card_header("Selected ad"), uiOutput("v_player"))))),

  nav_panel("Same script, 9 states",
    div(class = "container-xl py-3",
      h2("One template, different numbers"),
      p(class = "lede", HTML("Each America Connects state campaign runs the same 'Building Responsibly' Water and Energy scripts with the state name and a figure swapped in. The share of time data centers supposedly use no water for cooling ranges from 90% to 98%. The homes-powered figure ranges from 31,000 to 3 million. Most water spots also cite the same national figure: water infrastructure \"spending to exceed $4 billion by 2030\". None of the state percentages comes with a published source.")),
      layout_columns(col_widths = c(5, 7),
        card(card_header("'Don't use water for cooling X% of the time'"), plotOutput("p_pct", height = "320px")),
        card(card_header("Claim by state"), DTOutput("t_template"))))),

  nav_panel("Meta ads",
    div(class = "container-xl py-3",
      h2("Facebook & Instagram ads (Meta Ad Library)"),
      p(class = "lede", HTML("Energy, water and cost claims from Meta ads. Spend and impressions are Meta's ranges. For ads labeled as social-issue ads, Meta publishes who paid and the age, gender and location of the people reached. <b>The newest state 'Connects' water ads (Sept–Oct 2026), QTS's ads and Compass's 'We Agree' ads ran without that label</b>, so Meta publishes no payer, spend or audience for them.")),
      card(card_header("Who saw each ad: share of impressions by age (Meta)"), plotOutput("p_aud", height = "430px")),
      DTOutput("t_meta"), br(),
      h5("Ads found per sponsor (exact-phrase search, US, all dates)"), tableOutput("t_meta_n"))),

  nav_panel("Lawsuits & challenges",
    div(class = "container-xl py-3",
      h2("Legal and regulatory challenges to the claims"),
      p(class = "lede", "Lawsuits, investigations, public-records fights and leaks about the energy and water information data center companies present. The allegations described are not court findings. Use 'Find ads' with the lawsuit filter to see every ad tied to each case."),
      uiOutput("law_cards"))),

  nav_panel("About",
    div(class = "container-xl py-3", style = "max-width:860px",
      h2("Methods"),
      tags$ul(
        tags$li("Google Ads Transparency Center: advertiser 'America Connects' (AR15194143977281421313) and others, US, read Oct 29–30, 2026. Each video ad was mapped to its YouTube ID through the ad preview."),
        tags$li("YouTube: title, channel, length, views and publish date read from each video page on Oct 29–30, 2026. View counts change over time."),
        tags$li("Meta Ad Library: exact-phrase searches for each sponsor, plus keyword sweeps, US, all ads, read Oct 29–30, 2026. 'Paid for by', spend, impressions, age/gender and location shares come from each ad's 'See ad details' panel, read Oct 30, 2026. Meta publishes these only for ads labeled as social-issue, election or political ads."),
        tags$li("Transcripts are YouTube's auto-generated captions and may contain errors. The archive quotes only short excerpts, and the word cloud shows only word counts. Open the video for the full ad."),
        tags$li("'Reported' entries rely on news coverage of an ad whose original creative hasn't been archived yet.")),
      h4("Fact-check ratings"),
      p("These are the archive's editorial assessments, made against public sources that are linked on each row. They are not legal findings."),
      tags$table(class = "scale",
        tags$tr(tags$td(HTML(fc_chip("Disputed"))), tags$td("Contradicted by public evidence, or the subject of a lawsuit or regulatory investigation.")),
        tags$tr(tags$td(HTML(fc_chip("Missing context"))), tags$td("Literally accurate or partly true, but leaves out information that changes what a viewer would conclude.")),
        tags$tr(tags$td(HTML(fc_chip("Supported"))), tags$td("Consistent with independent published estimates. Caveats are noted.")),
        tags$tr(tags$td(HTML(fc_chip("No public data"))), tags$td("Specific enough to check, but the company or group hasn't published the data needed.")),
        tags$tr(tags$td(HTML(fc_chip("Not yet checked"))), tags$td("Checkable against public filings; not done yet.")),
        tags$tr(tags$td(HTML(fc_chip("Not checkable"))), tags$td("A pledge, slogan or vague statement with nothing concrete to test."))),
      p(class = "mt-2", "'Checkable' covers the first five ratings."),
      p("Data files are in ", code("data/"), ". Add rows to the CSVs and redeploy.")))
)

server <- function(input, output, session) {

  output$t_campaigns <- renderDT({
    d <- campaigns
    if (input$c_region != "All") d <- d[d$region == input$c_region, ]
    if (input$c_stype != "All")  d <- d[d$sponsor_type == input$c_stype, ]
    if (input$c_fc != "All")     d <- d[d$factcheck == input$c_fc, ]
    cc <- claim_class(d$claim_type)
    if (input$c_claim == "Energy") d <- d[cc %in% c("energy", "both"), ]
    if (input$c_claim == "Water")  d <- d[cc %in% c("water", "both"), ]
    if (input$c_claim == "Counter-claims") d <- d[cc == "counter", ]
    cc <- claim_class(d$claim_type)
    out <- data.frame(
      Ad = sprintf("<b>%s</b><br><small>Appears as <b>%s</b> · %s</small>", esc(d$title), esc(d$appears_as), esc(d$place)),
      Claim = sprintf('<span class="claim-chip c-%s">%s</span><br>%s', cc, esc(d$claim_type), esc(d$claim)),
      `Paid for by` = sprintf("%s<br><small class='text-muted'>%s</small>", esc(d$paid_for_by), esc(d$funding_disclosed)),
      `Fact-check` = fc_chip(d$factcheck, d$factcheck_note, d$factcheck_url),
      Lawsuit = law_chip(d$lawsuit_ids, d$lawsuit_role),
      Date = esc(d$date),
      Links = paste(link(d$url_primary, "Ad ↗"), link(d$url_source, "Source ↗"), sep = "<br>"), check.names = FALSE)
    datatable(out, escape = FALSE, rownames = FALSE, options = list(pageLength = 15, autoWidth = TRUE,
              columnDefs = list(list(width = "26%", targets = 1), list(width = "22%", targets = 3))))
  })

  # ---- Find ads
  ads_f <- reactive({
    d <- ads
    if (input$f_law == "Yes: any lawsuit") d <- d[d$in_lawsuit == "Yes", ]
    else if (input$f_law == "No") d <- d[d$in_lawsuit == "No", ]
    else if (input$f_law != "All") d <- d[grepl(input$f_law, nz(d$lawsuit_ids), fixed = TRUE), ]
    if (input$f_group != "All") d <- d[d$appears_as == input$f_group, ]
    if (input$f_area != "All")  d <- d[d$area == input$f_area, ]
    if (input$f_age != "All")   d <- d[d$age_profile == input$f_age, ]
    if (input$f_kind != "All")  d <- d[d$kind == input$f_kind, ]
    if (input$f_fc == "Checkable claims only") d <- d[d$checkable == "Yes", ]
    else if (input$f_fc != "All") d <- d[d$factcheck == input$f_fc, ]
    o <- switch(input$f_sort,
      law   = order(d$in_lawsuit != "Yes", nz(d$lawsuit_ids), d$appears_as),
      group = order(d$appears_as, d$kind),
      area  = order(d$area, d$appears_as),
      fc    = order(d$fc_rank, d$appears_as),
      date  = order(as.character(nz(d$date)), decreasing = TRUE))
    d[o, ]
  })
  output$t_ads <- renderDT({
    d <- ads_f()
    out <- data.frame(
      `Appears as` = sprintf("<b>%s</b><br><small>%s · %s</small>", esc(d$appears_as), esc(d$kind), esc(d$platform)),
      `Paid for by` = sprintf("%s<br><small class='text-muted'>%s</small>", esc(d$paid_for_by), esc(d$funding_disclosed)),
      `Who sees it` = sprintf("<b>%s</b><br><small>%s</small><br><small class='text-muted'>%s</small>", esc(d$area), esc(d$audience_who), esc(d$reach)),
      Claim = sprintf('<span class="claim-chip c-%s">%s</span><br>%s', claim_class(d$claim_type), esc(d$claim_type), esc(d$claim)),
      `Fact-check` = fc_chip(d$factcheck, d$factcheck_note, d$factcheck_url),
      Lawsuit = law_chip(d$lawsuit_ids, d$lawsuit_role),
      Date = esc(d$date), Link = link(d$url, "Open ↗"), check.names = FALSE)
    datatable(out, escape = FALSE, rownames = FALSE, options = list(pageLength = 20, ordering = TRUE, autoWidth = TRUE,
              columnDefs = list(list(width = "22%", targets = 3), list(width = "20%", targets = 4))))
  })
  output$dl_ads <- downloadHandler(filename = function() "data_center_ads_filtered.csv",
    content = function(f) write.csv(ads_f()[, setdiff(names(ads), c("fc_rank"))], f, row.names = FALSE, fileEncoding = "UTF-8"))

  # ---- Word cloud
  wf_f <- reactive({
    d <- wf
    if (input$w_group != "All") d <- d[d$appears_as == input$w_group, ]
    if (input$w_law != "All")   d <- d[d$in_lawsuit == input$w_law, ]
    if (input$w_kind != "All")  d <- d[d$kind == input$w_kind, ]
    if (input$w_fc != "All")    d <- d[d$factcheck == input$w_fc, ]
    d
  })
  w_agg <- reactive({
    d <- wf_f(); if (!nrow(d)) return(data.frame(word = character(), n = numeric()))
    a <- aggregate(n ~ word, d, sum); a[order(-a$n), ]
  })
  output$w_cloud <- renderPlot({
    a <- w_agg()
    if (nrow(a) < 3) { plot.new(); text(.5, .5, "Too few words for this filter"); return() }
    a <- head(a, input$w_max)
    pal <- c("#9a958a", "#5b4b9a", "#c26a00", "#1f6f9a", "#1b1b18")
    par(mar = c(0, 0, 0, 0))
    set.seed(7)
    wordcloud(a$word, a$n, scale = c(9, 1.1), min.freq = 1, random.order = FALSE, rot.per = 0.12, colors = pal, family = "sans")
  })
  output$w_top <- renderTable(setNames(head(w_agg(), 12), c("Word", "Count")), digits = 0)
  output$w_n <- renderUI(p(class = "text-muted small", length(unique(wf_f()$uid)), " ads in this selection."))

  # ---- YouTube
  vids <- reactive({
    d <- videos
    if (input$v_state != "All") d <- d[d$state == input$v_state, ]
    if (input$v_topic != "All") d <- d[d$topic == input$v_topic, ]
    if (input$v_group != "All") d <- d[d$appears_as == input$v_group, ]
    if (isTRUE(input$v_trans))  d <- d[d$transcribed == "yes", ]
    d
  })
  output$t_videos <- renderDT({
    d <- vids()
    out <- data.frame(State = esc(d$state), `Appears as` = esc(d$appears_as), Title = esc(d$title), Topic = esc(d$topic),
                      Views = d$views, `Fact-check` = fc_chip(d$factcheck),
                      `Ran as Google ad` = ifelse(is.na(d$google_ads_first_shown), "",
                                                  paste(d$google_ads_first_shown, "→", d$google_ads_last_shown)),
                      YouTube = link(d$youtube_url, "Watch ↗"), check.names = FALSE)
    datatable(out, escape = FALSE, rownames = FALSE, selection = "single",
              options = list(pageLength = 12, order = list(list(4, "desc")))) |> formatCurrency("Views", currency = "", digits = 0)
  })
  output$v_player <- renderUI({
    d <- vids(); s <- input$t_videos_rows_selected
    if (!length(s)) return(p(class = "text-muted", "Click a row to play the ad here."))
    v <- d[s, ]
    tagList(
      div(class = "video-wrap", tags$iframe(src = paste0("https://www.youtube-nocookie.com/embed/", v$youtube_id),
          allow = "encrypted-media; picture-in-picture", allowfullscreen = NA)),
      h5(class = "mt-3", v$title), p(tags$small(v$channel, " · published ", v$published, " · ", format(v$views, big.mark = ","), " views")),
      p(tags$small(tags$b("Paid for by: "), v$paid_for_by)),
      if (!is.na(v$key_claim) && nzchar(v$key_claim)) tags$blockquote(class = "border-start ps-2", v$key_claim)
      else p(class = "text-muted", "Script not yet transcribed."),
      HTML(fc_chip(v$factcheck, v$factcheck_note, v$factcheck_url)),
      if (!is.na(v$lawsuit_ids)) p(class = "mt-2", HTML(law_chip(v$lawsuit_ids, v$lawsuit_role))),
      p(class = "mt-2", tags$a(href = v$youtube_url, target = "_blank", "Open on YouTube ↗")))
  })

  output$p_pct <- renderPlot({
    d <- template[!is.na(template$water_pct), ]
    d <- d[order(d$water_pct), ]
    par(mar = c(4, 9, 1, 2), family = "sans")
    b <- barplot(d$water_pct, names.arg = d$state, horiz = TRUE, las = 1, xlim = c(0, 112), xpd = TRUE,
                 col = "#1f6f9a", border = NA, xlab = "% of the time (as claimed in the ad)")
    text(d$water_pct, b, paste0(d$water_pct, "%"), pos = 4, cex = .9)
  })
  output$t_template <- renderDT({
    yt <- function(id, lab) ifelse(is.na(id) | id == "", "", link(paste0("https://www.youtube.com/watch?v=", id), lab))
    out <- data.frame(State = esc(template$state), `Water claim` = esc(template$water_line),
                      `Homes powered by "new energy projects"` = esc(template$homes_powered),
                      Ads = paste(yt(template$water_video, "Water ↗"), yt(template$water_video_2, "Water (alt) ↗"),
                                  yt(template$energy_video, "Energy ↗"), sep = " "), check.names = FALSE)
    datatable(out, escape = FALSE, rownames = FALSE, options = list(dom = "t", pageLength = 20))
  })

  # ---- Meta
  output$p_aud <- renderPlot({
    a <- maud
    a$label <- paste0(a$paid_for_by, " · ", sub(" - .*", "", a$ran))
    a <- a[order(a$age_55_plus), ]
    m <- t(as.matrix(a[, c("age_18_34", "age_35_54", "age_55_plus")]))
    par(mar = c(4, 22, 2, 1), family = "sans", las = 1)
    barplot(m, horiz = TRUE, names.arg = a$label, col = c("#1f6f9a", "#9a958a", "#c26a00"), border = NA,
            xlim = c(0, 100), xlab = "% of impressions", cex.names = .8)
    legend("top", inset = -0.07, horiz = TRUE, xpd = TRUE, bty = "n", fill = c("#1f6f9a", "#9a958a", "#c26a00"),
           legend = c("18–34", "35–54", "55+"), border = NA, cex = .85)
  })
  output$t_meta <- renderDT({
    d <- meta_ads
    out <- data.frame(`Appears as` = esc(d$appears_as),
                      Claim = sprintf('<span class="claim-chip c-%s">%s</span><br>%s', claim_class(d$claim_type), esc(d$claim_type), esc(d$text)),
                      `Paid for by` = esc(d$paid_for_by),
                      `Who saw it` = sprintf("<b>%s</b><br><small>%s</small>", esc(d$audience_where), esc(d$audience_who)),
                      `Spend / reach` = esc(nz(d$reach)), `Fact-check` = fc_chip(d$factcheck, d$factcheck_note, d$factcheck_url),
                      Lawsuit = law_chip(d$lawsuit_ids, d$lawsuit_role),
                      `Ad record` = link(d$url, paste0("ID ", d$library_id, " ↗")), check.names = FALSE)
    datatable(out, escape = FALSE, rownames = FALSE, options = list(pageLength = 15, autoWidth = TRUE))
  })
  output$t_meta_n <- renderTable(setNames(meta_n, c("Sponsor", "Ads found")))

  output$law_cards <- renderUI({
    do.call(layout_column_wrap, c(list(width = 1/2), lapply(seq_len(nrow(lawsuits)), function(i) {
      l <- lawsuits[i, ]
      n_ads <- sum(grepl(l$id, nz(ads$lawsuit_ids), fixed = TRUE))
      card(class = "law-card",
        card_header(tags$small(class = "text-muted", l$type, " · ", l$filed), br(), tags$b(l$title)),
        p(tags$small(l$jurisdiction)), p(tags$b("Parties: "), l$parties),
        p(tags$b("What's challenged: "), l$claims_challenged), p(tags$b("Status: "), l$status),
        if (!is.na(l$links_to) && nzchar(l$links_to)) p(tags$small("Related archive entries: ", l$links_to, " · ", n_ads, " ad records in total")),
        tags$a(href = l$url, target = "_blank", "Source ↗"))
    })))
  })
}

shinyApp(ui, server)
