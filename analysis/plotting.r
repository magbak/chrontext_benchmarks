#Based on https://github.com/magbak/mbei-experiments/blob/main/ExperimentA/analysis.R
deps <- c("plyr","tidyverse")
packs <- installed.packages()

for (d in deps) {
  if (!(d %in% packs[,"Package"])) {
    install.packages(d)
  }
}
library(plyr)
library(tidyverse)

filename <- "/home/mag/repos/chrontext_benchmark/analysis/otit_benchmark_data.csv"
df <- read_csv(filename)
df <- df %>% pivot_longer(cols="3":"12", names_to="run")

query_df = tibble(query_number=1:4, n_turbines=c(1,10,100,400))

df <- df %>% mutate(query_number=str_extract(query,"[0-9]"))
df <- join(df, query_df, by="query_number")
df

df %>% drop_na(value) %>% group_by(solution, query) %>% dplyr::summarize(
  N=sum(!is.na(value)),
  mean=mean(value),
  sd=sd(value)
  ) %>% arrange(query, solution) %>% as.data.frame(.) %>% dplyr::mutate_if(is.numeric, round, 2)


df_prod_grouped <- df %>% filter(str_starts(query, "Production Grouped"))
df_prod_grouped

df_prod <- df %>% filter(!str_starts(query, "Production Grouped")) %>% filter(!str_starts(query, "Multi"))
df_prod

df_multi_grouped <- df %>% filter(str_starts(query, "Multi"))
df_multi_grouped

t1<-theme(                              
  plot.background = element_blank(), 
  #panel.grid.major = element_blank(), 
  #panel.grid.minor = element_blank(), 
  strip.background = element_blank(),
  #panel.border = element_blank(), 
  panel.background = element_blank(),
  axis.line = element_line(size=.4),
  strip.text.x = element_text(size=14),
  legend.position="bottom"
)

p_prod <- ggplot(df_prod, aes(x=n_turbines, y=value, shape=solution, color=solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_jitter(size=3, height=0, width=0.2) +
  labs(x="Number of wind turbines", y="Query processing time in seconds") +
  theme(text = element_text(size = 12)) +
  expand_limits(y=0)
p_prod

ggsave("/home/mag/repos/chrontext_benchmark/analysis/prod.png", p_prod, dpi=300, width=10, height=10, units="cm")

p_prod_grouped <- ggplot(df_prod_grouped, aes(x=n_turbines, y=value, shape=solution, color=solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_jitter(size=3, height=0, width=0.2) +
  labs(x="Number of wind turbines", y="Query processing time in seconds") +
  theme(text = element_text(size = 12)) +
  expand_limits(y=0)
p_prod_grouped

ggsave("/home/mag/repos/chrontext_benchmark/analysis/prod_grouped.png", p_prod_grouped, dpi=300, width =10, height=10, units="cm")

p_multi_grouped <- ggplot(df_multi_grouped, aes(x=n_turbines, y=value, shape=solution, color=solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_jitter(size=3, height=0, width=0.2) +
  labs(x="Number of wind turbines", y="Query processing time in seconds") +
  theme(text = element_text(size = 12)) +
  expand_limits(y=0) +
  scale_shape_manual(values=c(17)) + 
  scale_color_manual(values=c("#00BFC4"))
p_prod_grouped

ggsave("/home/mag/repos/chrontext_benchmark/analysis/multi_grouped.png", p_multi_grouped, dpi=300, width =10, height=10, units="cm")

