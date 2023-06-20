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

data_type_vect <- c(
	character = 'character',
	str = 'character',
	integer = 'integer',
	int = 'integer',
	logical = 'logical',
	bool = 'logical'
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

send <- function(conn, data, send_data_type = FALSE) {
	if (send_data_type) {
		data_type_name <- typeof(data)
		data_type_name <- convert_to_binary(data_type_name)
		writeBin(data_type_name, conn)
	}
	bin_data <- convert_to_binary(data)
	writeBin(bin_data, conn)
}

# Add optional expect_data_type argument that will receive and convert data type as string
# should there be an expected data type arg that specifies a known data type?
recv <- function(conn, recv_data_type = FALSE, set_data_type = "character") {
	if (recv_data_type) {
		suppressWarnings(data_type_name <- readBin(conn, "raw", HEADER))
		while (length(data_type_name) == 0) {
			suppressWarnings(data_type_name <- readBin(conn, "raw", HEADER))
		}
		data_type_name <- convert_from_binary(data_type_name, "character")
		data_type_name <- data_type_vect[data_type_name]
	} else {
		data_type_name <- set_data_type
	}

	suppressWarnings(data <- readBin(conn, "raw", HEADER))
	while (length(data) == 0) {
		suppressWarnings(data <- readBin(conn, "raw", HEADER))
	}

	data <- convert_from_binary(data, data_type_name)

	return(data)
}

#receive target file path
file_path <- recv(con)

#load target file
# need to learn how to receive path as system argument.
source(file_path)

confirm <- TRUE
msg <- 'confirm'

while (msg != '!DISCONNECT') {
	# there should be several handeling methods
		# returning variables
		# evaluating expressions
	display_msg(msg)
	val <- get(msg)
	send(con, val, TRUE)
	msg <- recv(con, FALSE, "character")
}

close(con)