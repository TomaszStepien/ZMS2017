# setwd("C:/python/zms/final/csv")
# list.files()

read_rondos <- function(){
    setwd("C:/python/zms/final/csv")
    x <- data.frame(arrival_time = numeric(), 
                    origin = character(), 
                    total_time = numeric(),
                    waiting_time = numeric(),
                    lw = numeric(),
                    le = numeric(),
                    ls = numeric(),
                    ln = numeric(),
                    capacity = numeric(),
                    size = numeric())
    l <- list.files()
    l = l[regexpr('_',l)==6]
    for(i in 1:length(l)){
        x1 <- read.csv(l[i])
        x1$lw = rep(substr(l[i], regexpr('w',l[i])+1, gregexpr('n',l[i])[[1]][2]-1))
        x1$le = rep(substr(l[i], regexpr('e',l[i])+1, regexpr('w',l[i])-1))
        x1$ls = rep(substr(l[i], regexpr('s',l[i])+1, gregexpr('_',l[i])[[1]][2]-1))
        x1$ln = rep(substr(l[i], gregexpr('n',l[i])[[1]][2]+1, regexpr('s',l[i])-1))
        x1$capacity = rep(substr(l[i], regexpr('c',l[i])+1, nchar(l[i])))
        x1$size = rep(substr(l[i], gregexpr('s',l[i])[[1]][2]+1, gregexpr('_',l[i])[[1]][3]-1))
        x1$simulation <- i
        x1$X <- NULL
        x <- rbind(x, x1)
    }
    return(x)
}

read_swiatla <- function(){
    setwd("C:/python/zms/final/csv")
    x <- data.frame(arrival_time = numeric(), 
                    origin = character(), 
                    total_time = numeric(),
                    waiting_time = numeric(),
                    lw = numeric(),
                    le = numeric(),
                    ls = numeric(),
                    ln = numeric(),
                    capacity = numeric(),
                    red = numeric(),
                    green = numeric())
    l <- list.files()
    l = l[regexpr('_',l)==8]
    for(i in 1:length(l)){
        x1 <- read.csv(l[i])
        x1$lw = rep(substr(l[i], gregexpr('w', l[i])[[1]][2]+1, regexpr('n', l[i])-1))
        x1$le = rep(substr(l[i], regexpr('e',l[i])+1, gregexpr('w',l[i])[[1]][2]-1))
        x1$ls = rep(substr(l[i], gregexpr('s',l[i])[[1]][2]+1, gregexpr('_',l[i])[[1]][2]-1))
        x1$ln = rep(substr(l[i], gregexpr('n',l[i])[[1]][1]+1, gregexpr('s',l[i])[[1]][2]-1))
        x1$capacity = rep(substr(l[i], regexpr('c',l[i])+1, nchar(l[i])))
        x1$red = rep(substr(l[i], gregexpr('r',l[i])[[1]][2]+1, gregexpr('g',l[i])[[1]][1]-1))
        x1$green = rep(substr(l[i], gregexpr('g',l[i])[[1]][1]+1, gregexpr('_',l[i])[[1]][4]-1))
        x1$simulation <- i
        x1$X <- NULL
        x <- rbind(x, x1)
    }
    return(x)
}
# x <- read.csv("rondo_le12w12n12s12_s12_c6")
# y <- read.csv("swiatla_le8w8n8s8_ru3-6_r55g50_c3")
# x$X <- NULL

ronda <- read_rondos()
swiatla <- read_swiatla()
