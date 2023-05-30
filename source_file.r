display_msg <- function(msg) {
    cat(
        '\033[94m',
        msg,
        sep = '',
        end = '\033[0m\n'
    )
}

msg <- "hello world - R"

display_msg(msg)
