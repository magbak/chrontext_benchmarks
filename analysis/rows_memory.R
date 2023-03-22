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

filename <- "/home/magbak/repos/chrontext_benchmarks/analysis/number_of_rows.csv"

df <- read_csv(filename)

query_df = tibble(query_number=1:4, n_turbines=c(1,10,100,400))

df <- df %>% mutate(query_number=str_extract(Query,"[0-9]"))
df <- join(df, query_df, by="query_number")
df <- df %>% mutate(Rows = RowsReal + RowsBool)
df

df_prod_grouped <- df %>% filter(str_starts(Query, "Production Grouped"))
df_prod_grouped

df_prod <- df %>% filter(!str_starts(Query, "Production Grouped"))
df_prod


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

p_prod_rows <- ggplot(df_prod, aes(x=n_turbines, y=Rows, fill=Solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  scale_y_continuous(breaks=c(0, 10000000,20000000,30000000,40000000,50000000,60000000,70000000,80000000,90000000,100000000)) +
  theme_bw() +
  t1 + 
  geom_bar(stat = "identity", position=position_dodge()) +
  labs(x="Number of wind turbines", y="Number of rows scanned") +
  theme(text = element_text(size = 12), legend.position = "bottom", legend.direction = "horizontal") +
  expand_limits(y=0) + 
  scale_fill_manual(values=c("#00BFC4","#f8766d","#619cff"))
p_prod_rows


ggsave("/home/magbak/Documents/prod_rows.png", p_prod_rows, dpi=300, width=10, height=10, units="cm")

p_prod_mem <- ggplot(df_prod, aes(x=n_turbines, y=Memory, fill=Solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_bar(stat = "identity", position=position_dodge()) +
  labs(x="Number of wind turbines", y="Total Dremio Memory (MB)") +
  theme(text = element_text(size = 12), legend.position = "bottom", legend.direction = "horizontal") +
  expand_limits(y=0) + 
  scale_fill_manual(values=c("#00BFC4","#f8766d","#619cff"))
p_prod_mem

ggsave("/home/magbak/Documents/prod_mem.png", p_prod_mem, dpi=300, width=10, height=10, units="cm")

p_prod_time <- ggplot(df_prod, aes(x=n_turbines, y=Time, fill=Solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_bar(stat = "identity", position=position_dodge()) +
  labs(x="Number of wind turbines", y="Dremio Execution Time in seconds") +
  theme(text = element_text(size = 12), legend.position = "bottom", legend.direction = "horizontal") +
  expand_limits(y=0) + 
  scale_fill_manual(values=c("#00BFC4","#f8766d","#619cff"))
p_prod_time

ggsave("/home/magbak/Documents/prod_time.png", p_prod_time, dpi=300, width=10, height=10, units="cm")


p_prod_grouped_rows <- ggplot(df_prod_grouped, aes(x=n_turbines, y=Rows, fill=Solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_bar(stat = "identity", position=position_dodge()) +
  labs(x="Number of wind turbines", y="Query time in seconds") +
  theme(text = element_text(size = 12)) +
  expand_limits(y=0) + 
  scale_shape_manual(values=c(17,16)) + 
  scale_color_manual(values=c("#00BFC4", "#f8766d"))
p_prod_grouped

ggsave("/home/magbak/Documents/prod_grouped_rows.png", p_prod_grouped_rows, dpi=300, width =10, height=10, units="cm")

p_prod_grouped_mem <- ggplot(df_prod_grouped, aes(x=n_turbines, y=Memory, fill=Solution)) + 
  scale_x_continuous(trans="log10", breaks = c(1,10,100,400)) +
  theme_bw() +
  t1 + 
  geom_bar(stat = "identity", position=position_dodge()) +
  labs(x="Number of wind turbines", y="Query time in seconds") +
  theme(text = element_text(size = 12)) +
  expand_limits(y=0) + 
  scale_shape_manual(values=c(17,16)) + 
  scale_color_manual(values=c("#00BFC4", "#f8766d"))
p_prod_grouped_mem

ggsave("/home/magbak/Documents/prod_grouped_mem.png", p_prod_grouped_mem, dpi=300, width =10, height=10, units="cm")



