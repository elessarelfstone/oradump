import time


def logging(table, source_code, logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info("Data extraction started for {} table from {} source".format(table, source_code))
            res = func(*args, **kwargs)
            logger.info("Data extraction successfully ended for {} table from {} source".format(table, source_code))
            logger.info("csv rows count:{} check sum:{}".format(res[2], res[3]))
            return res
        return wrapper
    return decorator


def benchmark(logger, measure="mins"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            time_repr = "Elapsed time : {} minutes {} seconds"
            if measure == "mins":
                time_repr = time_repr.format(divmod(end-start, 60)[0], int(divmod(end-start, 60)[1]))
            logger.debug(time_repr)
            return result
        return wrapper
    return decorator


def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                raise
        return wrapper
    return decorator
