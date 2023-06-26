HEADER <- 2048
PORT <- 6011
SERVER <- "localhost"
FORMAT <- "utf-8"
DISCONNECT_MESSAGE <- "!DISSCONNECT"
UUID <- commandArgs(trailingOnly = TRUE)[1]
TARGET_FILE <- commandArgs(trailingOnly = TRUE)[2]

data_type_vect <- c(
	character = 'character',
	str = 'character',
	integer = 'integer',
	int = 'integer',
	logical = 'logical',
	bool = 'logical'
)

display_msg <- function(...) {
	cat('\033[94m')
	cat(
        ...,
        end = '\033[0m\n'
    )
}

add_missing_bits <- function(bits, base = 8) {
	missing_bits <- length(bits) %% base
	if (missing_bits > 0) {
		missing_bits <- rep(as.raw(00), times = base - missing_bits)
		bits <- c(bits, missing_bits)
	}
	return(bits)
}

bin_conv <- function(data, data_type_name = NA) {
	conv_data <- NA
	# convert to binary
	if (is.character(data) && is.na(data_type_name)) {
		conv_data <- charToRaw(data)
		conv_data <- rawToBits(conv_data)
	} else if (is.integer(data) && is.na(data_type_name)) {
		conv_data <- as.raw(data)
		conv_data <- rawToBits(conv_data)
	} else if (is.logical(data) && is.na(data_type_name)) {
		conv_data <- as.raw(data)
		conv_data <- rawToBits(conv_data)
	# convert from binary
	} else if (is.raw(data) && data_type_name == "character") {
		conv_data <- add_missing_bits(data)
		conv_data <- packBits(conv_data, "raw")
		conv_data <- rawToChar(conv_data)
	} else if (is.raw(data) && data_type_name == "integer") {
		conv_data <- add_missing_bits(data)
		conv_data <- packBits(conv_data, "raw")
		conv_data <- as.integer(conv_data)
	} else if (is.raw(data) && data_type_name == "logical") {
		conv_data <- add_missing_bits(data)
		conv_data <- packBits(conv_data, "raw")
		conv_data <- as.logical(conv_data)
	}
	return(conv_data)
}

# may not need to pass connection if it will only be 1 per dialogue
send <- function(conn, data, send_data_type = FALSE) {
	if (send_data_type) {
		data_type_name <- typeof(data)
		data_type_name <- bin_conv(data_type_name)
		writeBin(data_type_name, conn)
	}
	bin_data <- bin_conv(data)
	writeBin(bin_data, conn)
}

# may not need to pass connection if it will only be 1 per dialogue
# I still want to consolidate the recv_data_type and set_data_type args
recv <- function(conn, recv_data_type = FALSE, set_data_type = "character") {
	if (recv_data_type) {
		suppressWarnings(data_type_name <- readBin(conn, "raw", HEADER))
		while (length(data_type_name) == 0) {
			suppressWarnings(data_type_name <- readBin(conn, "raw", HEADER))
		}
		data_type_name <- bin_conv(data_type_name, "character")
		data_type_name <- data_type_vect[data_type_name]
	} else {
		data_type_name <- set_data_type
	}

	suppressWarnings(data <- readBin(conn, "raw", HEADER))
	while (length(data) == 0) {
		suppressWarnings(data <- readBin(conn, "raw", HEADER))
	}

	data <- bin_conv(data, data_type_name)

	return(data)
}

find_connection <- function() {
	connected <- FALSE
	while (!connected) {
		con <- socketConnection(
			host = SERVER,
			port = PORT,
			server = FALSE,
			open = "a+b"
		)

		send(con, UUID)
		uuid_chk <- recv(con)
		connected <- (UUID == uuid_chk)
		if (!connected) {
			close(con)
		}
	}
	return(con)
}

import_variable <- function() {
	var_name <- recv(con, FALSE, "character")
	var_val <- get(var_name)
	send(con, var_val, TRUE)
}

evaluate_expression <- function () {
	arg_count <- recv(con, FALSE, "integer")
	send(con, TRUE)
	method_name <- recv(con, FALSE, "character")
	send(con, TRUE)
	args <- list()
	if (arg_count > 0) {
		for (i in 1:arg_count) {
		args <- c(args, recv(con, TRUE))
		send(con, TRUE)
		}
	}
	result <- do.call(method_name, args)
	send(con, result, TRUE)
}

con <- find_connection()

#load target file
source(TARGET_FILE)

send(con, TRUE)

cmd_int <- -1
while (cmd_int != 0) {
	cmd_int <- recv(con, FALSE, "integer")
	if (cmd_int == 1){
		send(con, TRUE)
		import_variable()
	} else if (cmd_int == 2) {
		send(con, TRUE)
		evaluate_expression()
	}
}

close(con)