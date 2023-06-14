HEADER <- 2048
PORT <- 6011
SERVER <- "localhost"
FORMAT <- "utf-8"
DISCONNECT_MESSAGE <- "!DISSCONNECT"

con <- socketConnection(
	host = SERVER,
	port = PORT,
	server = FALSE,
	open = "a+b"
)

display_msg <- function(msg) {
    cat(
        '\033[94m',
        msg,
        sep = '',
        end = '\033[0m\n'
    )
}

add_missing_bits <- function(bin_data, base = 8) {
	missing_bits <- length(bin_data) %% base
	if (missing_bits > 0) {
		missing_bits <- rep(as.raw(00), times = base - missing_bits)
		bin_data <- c(bin_data, missing_bits)
	}
	return(bin_data)
}

convert_from_binary <- function(bin_data, to_type) {
	data <- NA
	bin_data <- add_missing_bits(bin_data)
	if (to_type == "character") {
		data <- packBits(bin_data, "raw")
		data <- rawToChar(data)
	} else if (to_type == "integer") {
		data <- packBits(bin_data, "raw")
		data <- as.integer(data)
	}
	return(data)
}

convert_to_binary <- function(data) {
	bin_data <- NA
	if (is.character(data)) {
		bin_data <- charToRaw(data)
		bin_data <- rawToBits(bin_data)
	} else if (is.integer(data)) {
		bin_data <- as.raw(data)
		bin_data <- rawToBits(bin_data)
	}
	return(bin_data)
}

send <- function(conn, data) {
	writeBin(data, conn)
}

recv <- function(conn, silent = TRUE) {
	if (silent) {
		suppressWarnings(data <- readBin(conn, "raw", HEADER))
		while (length(data) == 0) {
			suppressWarnings(data <- readBin(conn, "raw", HEADER))
		}
	} else {
		data <- readBin(conn, "raw", HEADER)
		while (length(data) == 0) {
			cat('ALERT\n')
			data <- readBin(conn, "raw", HEADER)
		}
	}
	return(data)
}

#receive target file path
file_path <- recv(con)
file_path <- convert_from_binary(file_path, "character")

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
	val <- convert_to_binary(val)
	send(con, val)
	msg <- recv(con)
	msg <- convert_from_binary(msg, "character")
}

close(con)