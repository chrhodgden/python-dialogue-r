HEADER <- 256
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

send <- function(conn, msg) {
	sendme <- paste(msg, strrep(" ", HEADER - nchar(msg)), sep = "")
	writeChar(sendme, conn)
}

recv <- function(conn) {
	suppressWarnings(msg <- trimws(readChar(conn, HEADER)))
	while (length(msg) == 0) {
		#cat('ALERT\n')
		suppressWarnings(msg <- trimws(readChar(conn, HEADER)))
	}
	return(msg)
}

#receive target file path
file_path <- recv(con)

#load target file
source(file_path)

confirm <- TRUE
msg <- 'confirm'

while (msg != '!DISCONNECT') {
	# there should be several handeling methods
		# returning variables
		# evaluating expressions
	display_msg(msg)
	val <- get(msg)
	val <- as.character(val)
	send(con, val)
	msg <- recv(con)
}

close(con)