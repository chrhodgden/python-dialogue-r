HEADER <- 2048
PORT <- 6011
SERVER <- "localhost"
FORMAT <- "utf-8"
DISCONNECT_MESSAGE <- "!DISSCONNECT"
UUID <- commandArgs(trailingOnly = TRUE)[1]
TARGET_FILE <- commandArgs(trailingOnly = TRUE)[2]

data_type_vect <- c(
	character = "character",
	str = "character",
	integer = "integer",
	int = "integer",
	double = "double",
	float = "double",
	logical = "logical",
	bool = "logical"
)

display_msg <- function(...) {
	cat("\033[94m")
	cat(
        ...,
        end = "\033[0m\n"
    )
}

# may not need to pass connection if it will only be 1 per dialogue
send <- function(conn, data, send_data_type = FALSE) {
	if (send_data_type) {
		data_type_name <- typeof(data)
		writeBin(data_type_name, conn)
		recv_chk <- recv(conn, set_data_type = 'logical')
	}
	writeBin(data, conn)
}

# may not need to pass connection if it will only be 1 per dialogue
# I still want to consolidate the recv_data_type and set_data_type args
recv <- function(conn, recv_data_type = FALSE, set_data_type = "character") {
	if (recv_data_type) {
		suppressWarnings(data_type <- readBin(conn, "raw", HEADER))
		while (length(data_type) == 0) {
			suppressWarnings(data_type <- readBin(conn, "raw", HEADER))
		}
		data_type <- readBin(data_type, "character")
		data_type <- data_type_vect[data_type]
		send(con, TRUE)
	} else {
		data_type <- set_data_type
	}

	suppressWarnings(data <- readBin(conn, "raw", HEADER))
	while (length(data) == 0) {
		suppressWarnings(data <- readBin(conn, "raw", HEADER))
	}

	data <- readBin(data, data_type)

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

evaluate_expression <- function() {
	arg_count <- recv(con, FALSE, "integer")
	send(con, TRUE)
	kwarg_count <- recv(con, FALSE, "integer")
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
	kwargs <- list()
	if (kwarg_count > 0) {
		keys <- c()
		vals <- list()
		for (i in 1:kwarg_count) {
			keys <- c(keys, recv(con))
			send(con, TRUE)
			vals <- c(vals, recv(con, TRUE))
			send(con, TRUE)
		}
		kwargs <- setNames(vals, keys)
	}
	args <- c(args, kwargs)
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