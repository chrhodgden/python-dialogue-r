dialoguer.HEADER <- 2048
dialoguer.PORT <- 6011
dialoguer.SERVER <- "localhost"
dialoguer.UUID <- commandArgs(trailingOnly = TRUE)[1]
dialoguer.TARGET_FILE <- commandArgs(trailingOnly = TRUE)[2]

dialoguer.data_type_vect <- c(
	character = "character",
	str = "character",
	integer = "integer",
	int = "integer",
	double = "double",
	float = "double",
	logical = "logical",
	bool = "logical"
)

dialoguer.display_msg <- function(...) {
	cat("\033[94m")
	cat(
        ...,
        end = "\033[0m\n"
    )
}

dialoguer.sub_send <- function(conn, data) {
	writeBin(data, conn)
}

# may not need to pass connection if it will only be 1 per dialogue
dialoguer.send <- function(conn, data, send_data_type = FALSE, send_length = FALSE, send_element_names = FALSE) {
	if (send_data_type) {
		data_type_name <- typeof(data)
		dialoguer.sub_send(conn, data_type_name)
		recv_chk <- dialoguer.sub_recv(conn, 'logical')
	}
	if (send_length) {
		data_length <- length(data)
		dialoguer.sub_send(conn, data_length)
		recv_chk <- dialoguer.sub_recv(conn, 'logical')
	}
	if (send_element_names) {
		data_names_length <- length(names(data))
		dialoguer.sub_send(conn, data_names_length)
		recv_chk <- dialoguer.sub_recv(conn, 'logical')
		if (data_names_length) {
			for (elem_name in names(data)) {
				dialoguer.sub_send(conn, elem_name)
				recv_chk <- dialoguer.sub_recv(conn, 'logical')
			}
		}
	}
	for (elem in data) {
		dialoguer.sub_send(conn, elem)
		recv_chk <- dialoguer.sub_recv(conn, 'logical')
	}
}

dialoguer.sub_recv <- function(conn, data_type = "character") {
	suppressWarnings(data <- readBin(conn, "raw", dialoguer.HEADER))
	while (length(data) == 0) {
		suppressWarnings(data <- readBin(conn, "raw", dialoguer.HEADER))
	}
	data <- readBin(data, data_type)
	return(data)
}

# may not need to pass connection if it will only be 1 per dialogue
# I still want to consolidate the recv_data_type and set_data_type args
dialoguer.recv <- function(conn, recv_data_type = FALSE, set_data_type = "character", recv_length = FALSE, recv_element_names = FALSE) {
	if (recv_data_type) {
		data_type <- dialoguer.sub_recv(conn)
		dialoguer.sub_send(conn, TRUE)
		data_type <- dialoguer.data_type_vect[data_type]
	} else {
		data_type <- set_data_type
	}

	if (recv_length) {
		data_length <- dialoguer.sub_recv(conn, "integer")
		dialoguer.sub_send(conn, TRUE)
	} else {
		data_length <- 1
	}

	data <- c()
	for (i in 1:data_length) {
		elem <- dialoguer.sub_recv(conn, data_type)
		dialoguer.sub_send(conn, TRUE)
		data <- c(data, elem)
	}

	if (recv_element_names) {
		data_names_length <- dialoguer.sub_recv(conn, "integer")
		dialoguer.sub_send(conn, TRUE)
		elem_names <- c()
		for (i in 1:data_names_length) {
			elem_name <- dialoguer.sub_recv(conn)
			dialoguer.sub_send(conn, TRUE)
			elem_names <- c(elem_names, elem_name)
		}
		names(data) <- elem_names
	}

	return(data)
}

dialoguer.find_connection <- function() {
	connected <- FALSE
	while (!connected) {
		conn <- socketConnection(
			host = dialoguer.SERVER,
			port = dialoguer.PORT,
			server = FALSE,
			open = "a+b"
		)

		dialoguer.send(conn, dialoguer.UUID)
		dialoguer.sub_send(conn, TRUE)
		uuid_chk <- dialoguer.recv(conn)
		connected <- (dialoguer.UUID == uuid_chk)
		if (!connected) {
			close(conn)
		}
	}
	return(conn)
}

dialoguer.import_variable <- function() {
	var_name <- dialoguer.recv(dialoguer.con, FALSE, "character")
	var_val <- get(var_name)
	dialoguer.send(dialoguer.con, var_val, TRUE, TRUE, TRUE)
}

dialoguer.assign_variable <- function() {
	var_name <- dialoguer.recv(dialoguer.con, FALSE, "character")
	dialoguer.send(dialoguer.con, TRUE)
	var_val <- dialoguer.recv(dialoguer.con, TRUE)
	dialoguer.send(dialoguer.con, TRUE)
	assign(var_name, var_val, envir = globalenv())
}

dialoguer.evaluate_expression <- function() {
	arg_count <- dialoguer.recv(dialoguer.con, FALSE, "integer")
	dialoguer.send(dialoguer.con, TRUE)
	kwarg_count <- dialoguer.recv(dialoguer.con, FALSE, "integer")
	dialoguer.send(dialoguer.con, TRUE)
	method_name <- dialoguer.recv(dialoguer.con, FALSE, "character")
	dialoguer.send(dialoguer.con, TRUE)
	args <- list()
	if (arg_count > 0) {
		for (i in 1:arg_count) {
		args <- c(args, dialoguer.recv(dialoguer.con, TRUE))
		dialoguer.send(dialoguer.con, TRUE)
		}
	}
	kwargs <- list()
	if (kwarg_count > 0) {
		keys <- c()
		vals <- list()
		for (i in 1:kwarg_count) {
			keys <- c(keys, dialoguer.recv(dialoguer.con))
			dialoguer.send(dialoguer.con, TRUE)
			vals <- c(vals, dialoguer.recv(dialoguer.con, TRUE))
			dialoguer.send(dialoguer.con, TRUE)
		}
		kwargs <- setNames(vals, keys)
	}
	args <- c(args, kwargs)
	result <- do.call(method_name, args)
	dialoguer.send(dialoguer.con, result, TRUE)
}

dialoguer.save_environment <- function() {
	file_name <- dialoguer.recv(dialoguer.con, FALSE, "character")
	dialoguer.send(dialoguer.con, TRUE)
	all_vars <- ls(envir = globalenv())
	exclude_vars <- all_vars[grep("dialoguer\\.", all_vars)]
	vars_to_save <- setdiff(all_vars, exclude_vars)
	save(list = vars_to_save, file = file_name, envir = globalenv())
}

dialoguer.con <- dialoguer.find_connection()

#load target file
source(dialoguer.TARGET_FILE)

dialoguer.send(dialoguer.con, TRUE)

dialoguer.cmd_int <- -1
while (dialoguer.cmd_int != 0) {
	dialoguer.cmd_int <- dialoguer.recv(dialoguer.con, FALSE, "integer")
	if (dialoguer.cmd_int == 1){
		dialoguer.send(dialoguer.con, TRUE)
		dialoguer.import_variable()
	} else if (dialoguer.cmd_int == 2) {
		dialoguer.send(dialoguer.con, TRUE)
		dialoguer.assign_variable()
	} else if (dialoguer.cmd_int == 3) {
		dialoguer.send(dialoguer.con, TRUE)
		dialoguer.evaluate_expression()
	} else if (dialoguer.cmd_int == 4) {
		dialoguer.send(dialoguer.con, TRUE)
		dialoguer.save_environment()
	}
}

close(dialoguer.con)