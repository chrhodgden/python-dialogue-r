test_method <- function(arg_1, arg_2) {
	result <- arg_1 + arg_2
	return(result)
}

test_kwargs <- function(arg_1 = 1, arg_2 = 1) {
	result <- arg_1 * arg_2
	return(result)
}

test_args_and_kwargs <- function(arg_1, arg_2, kwarg_1 = 1., kwarg_2 = 3) {
	result <- arg_1 * arg_2
	result <- result * kwarg_1
	result <- result * kwarg_2
	return(result)
}
