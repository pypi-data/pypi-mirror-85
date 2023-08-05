from shield34_reporter.container.run_report_container import RunReportContainer

def get_shield34_proxy(upsream_chained_proxy=None):
    from shield34_reporter.utils.reporter_proxy import ProxyServerNotInitializedException, \
        create_new_proxy_instance
    proxies_count = len(RunReportContainer.get_current_block_run_holder().proxyServers)
    if proxies_count > 0:
        proxy_server = RunReportContainer.get_current_block_run_holder().proxyServers[proxies_count-1]

    if upsream_chained_proxy is not None:
        proxy_server = create_new_proxy_instance(upsream_chained_proxy)
        RunReportContainer.get_current_block_run_holder().proxyServers.append(proxy_server)


    if proxy_server is None:
        raise ProxyServerNotInitializedException()

    default_proxy = proxy_server.proxy
    http_proxy = "http://{}".format(default_proxy)
    https_proxy = "http://{}".format(default_proxy)
    ftp_proxy = "http://{}".format(default_proxy)
    proxyDict = {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }
    return proxyDict

