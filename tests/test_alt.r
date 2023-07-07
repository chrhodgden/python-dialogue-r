chk_0 <- TRUE

add_to_vector <- function(vect_name, val) {
	vect <- get(vect_name, envir = globalenv())
	vect <- c(vect, val)
	assign(vect_name, vect, envir = globalenv())
	return(TRUE)
}

display_vector <- function(vect_name) {
	vect <- get(vect_name, envir = globalenv())
	display_msg(vect)
	return(TRUE)
}

no_return_method <- function(i) {
	
}