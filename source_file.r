HEADER <- 64
PORT <- 6011
SERVER <- "localhost"
FORMAT <- "utf-8"
DISCONNECT_MESSAGE <- "!DISSCONNECT"

con <- socketConnection(
	host = SERVER,
	port = PORT,
	server = FALSE
)

display_msg <- function(msg) {
    cat(
        '\033[94m',
        msg,
        sep = '',
        end = '\033[0m\n'
    )
}

send_msg <- function(conn, msg) {
	sendme <- paste(msg, strrep(" ", HEADER - nchar(msg)), sep = "")
	writeChar(sendme, conn)
}

recv_msg <- function(conn) {
	suppressWarnings(msg <- trimws(readChar(conn, HEADER)))
	while (length(msg) == 0) {
		#cat('ALERT\n')
		suppressWarnings(msg <- trimws(readChar(conn, HEADER)))
	}
	return(msg)
}

msg <- "Initializing Client - R"
display_msg(msg)

msg <- "Initialized Client - R"
send_msg(con, msg)

while (msg != '!DISCONNECT') {
	msg <- recv_msg(con)
	display_msg(msg)
}

close(con)