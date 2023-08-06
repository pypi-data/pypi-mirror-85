import time

import json
import os
import pickle
import platform
import stat
import sys
import tempfile

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.proxy.browsermobproxy import Server
from shield34_reporter.utils.logger import Shield34Logger
from shield34_reporter.utils.network_utils import NetworkUtils
import urllib
import socket

class ProxyServerNotInitializedException(Exception):
    pass

class ProxyManagementServerNotInitializedException(Exception):
    pass

class ReporterProxy():

    local_ip = None
    browser_mob_server = None

    @staticmethod
    def get_ip():
        binding_server_mode = Shield34Properties.binding_server_mode
        if binding_server_mode == 'local':
            ReporterProxy.local_ip = "127.0.0.1"
        elif binding_server_mode == 'remote':
            if ReporterProxy.local_ip is None:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    # doesn't even have to be reachable
                    s.connect(('10.255.255.255', 1))
                    IP = s.getsockname()[0]
                except:
                    try:
                        IP = socket.gethostbyname(socket.gethostname())
                    except:
                        IP = '127.0.0.1'
                finally:
                    s.close()
                ReporterProxy.local_ip = IP
        return ReporterProxy.local_ip

    @staticmethod
    def browser_mob_proxy_is_listening(browser_mob_server,retry_count=60):
        count = 0
        while not ReporterProxy.browser_mob_server._is_listening():
            time.sleep(0.5)
            count += 1
            if count == retry_count:
                return False
        return True

    @staticmethod
    def start_proxy_management_server():
        if SdkAuthentication.is_authorized():
            from shield34_reporter.container.run_report_container import RunReportContainer
            block_run_report_container = RunReportContainer.get_current_block_run_holder()
            if Shield34Properties.binding_server_mode == 'local':
                if ReporterProxy.browser_mob_server is None:
                    block_run_report_container.proxyServers = []
                    proxy_exec_path = ReporterProxy.add_browsermob_to_path()
                    proxy_data_filepath = ReporterProxy.get_shield34_proxy_data_filename()
                    browser_mob_server_config = {}

                    ReporterProxy.wait_for_lock_create_proxy_to_be_released(timeout=10)

                    ReporterProxy.lock_create_proxy()
                    if os.path.exists(proxy_data_filepath):
                        try:
                            browser_mob_server_config = ReporterProxy.read_json_from_file(proxy_data_filepath)
                            if browser_mob_server_config.get('port',None) is not None and browser_mob_server_config.get('pid',None) is not None:
                                Shield34Logger.logger.console("\nUsing Shield34 Proxy Management Server on port {}".format(browser_mob_server_config['port']))
                                ReporterProxy.browser_mob_server = Server(proxy_exec_path,
                                                            options={'port': browser_mob_server_config['port']})
                                ReporterProxy.browser_mob_server.host = ReporterProxy.get_ip()
                                ReporterProxy.browser_mob_server.command += ['--address=' + ReporterProxy.get_ip(),"--ttl=3600"]

                                ReporterProxy.browser_mob_server.pid = browser_mob_server_config['pid']
                            else:
                                ReporterProxy.browser_mob_server = None
                        except Exception as e:
                            ReporterProxy.browser_mob_server = None

                    if ReporterProxy.browser_mob_server is None or not ReporterProxy.browser_mob_proxy_is_listening(ReporterProxy.browser_mob_server,retry_count=5):
                        if browser_mob_server_config.get('port',None) is not None:
                            Shield34Logger.logger.console("Shield34 Proxy Management Server not found on port {}".format(browser_mob_server_config['port']))
                        proxy_server_port = NetworkUtils.get_random_port(ReporterProxy.get_ip())
                        Shield34Logger.logger.console("Starting new Shield34 Proxy Management Server on port {}".format(proxy_server_port))
                        ReporterProxy.browser_mob_server = Server(proxy_exec_path,
                                                        options={'port': proxy_server_port})
                        ReporterProxy.browser_mob_server.host = ReporterProxy.get_ip()
                        ReporterProxy.browser_mob_server.command += ['--address='+ReporterProxy.get_ip(),"--ttl=3600"]

                        ReporterProxy.browser_mob_server.start()
                        browser_mob_server_config['port'] = proxy_server_port
                        browser_mob_server_config['pid'] = ReporterProxy.browser_mob_server.process.pid
                        ReporterProxy.browser_mob_server.pid = ReporterProxy.browser_mob_server.process.pid
                        try:
                            ReporterProxy.write_json_to_file(proxy_data_filepath, browser_mob_server_config)
                        except Exception as e:
                            pass

                    ReporterProxy.release_lock_create_proxy()

                    if ReporterProxy.browser_mob_server is None:
                        raise ProxyManagementServerNotInitializedException

                    #starting proxy instance
                    system_proxy = ReporterProxy.get_os_proxies()
                    proxy_server_instance = create_new_proxy_instance(system_proxy)
                    block_run_report_container.proxyServers.append(proxy_server_instance)

                    return True
                else:
                    # proxy management server already running
                    if len(block_run_report_container.proxyServers) == 0:
                        # starting proxy instance
                        system_proxy = ReporterProxy.get_os_proxies()
                        proxy_server_instance = create_new_proxy_instance(system_proxy)
                        block_run_report_container.proxyServers.append(proxy_server_instance)

                    return True
        return False



    @staticmethod
    def write_object_to_file(file_path, obj):
        pickle_out = open(file_path, "wb")
        pickle.dump(obj, pickle_out)
        pickle_out.close()

    @staticmethod
    def load_object_from_file(file_path):
        pickle_in = open(file_path, "rb")
        return pickle.load(pickle_in)

    @staticmethod
    def lock_create_proxy():
        ReporterProxy.write_lock_file(ReporterProxy.get_shield34_proxy_lock_filename())

    @staticmethod
    def release_lock_create_proxy():
        file =ReporterProxy.get_shield34_proxy_lock_filename()
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def wait_for_lock_create_proxy_to_be_released(timeout=10):
        counter = 0
        while os.path.exists(ReporterProxy.get_shield34_proxy_lock_filename()):
            time.sleep(1)
            counter = counter + 1
            if counter > timeout:
                ReporterProxy.release_lock_create_proxy()
                break



    @staticmethod
    def get_shield34_proxy_lock_filename():
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, 'shield34_proxy.lck')
        return filepath

    @staticmethod
    def get_shield34_proxy_data_filename():
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, 'shield34_proxy.dat')
        return filepath

    @staticmethod
    def write_json_to_file(file_path, dictjson):
        with open(file_path, 'w') as file:
            file.write(json.dumps(dictjson))
        file.close()

    @staticmethod
    def write_lock_file(file_path):
        with open(file_path, 'w') as file:
            file.write("")
        file.close()

    @staticmethod
    def read_json_from_file(file_path):
        with open(file_path, 'r') as file:
            dictjsonstr = file.read()
        file.close()
        return json.loads(dictjsonstr)

    @staticmethod
    def get_os_proxies():
        if Shield34Properties.selenium_proxy_address is not None:
            return Shield34Properties.selenium_proxy_address

        if sys.version_info > (3, 0):
            proxies = urllib.request.getproxies()
        else:
            proxies = urllib.getproxies()

        if 'https' in proxies:
            proxy = proxies['https']
            proxy = proxy.replace("https://", "")
            return proxy
        elif 'http' in proxies:
            proxy = proxies['http']
            proxy = proxy.replace("http://", "")
            return proxy
        else:
            return None

    @staticmethod
    def add_browsermob_to_path():
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(ROOT_DIR, 'proxy', 'browsermob-proxy-2.1.4', 'bin')
        os.environ["PATH"] += os.pathsep + path
        #Shield34Logger.logger.console("added '{}' to the system environment path".format(path))
        try:
            if platform.system() != 'Windows':
                file = os.path.join(path, "browsermob-proxy")
                st = os.stat(file)
                os.chmod(file, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            pass

        return os.path.join(path,'browsermob-proxy')


def create_new_proxy_instance(upstream_chained_proxy=None):
    sub_instance_port = NetworkUtils.get_random_port(ReporterProxy.get_ip())
    if upstream_chained_proxy is not None:
        proxy = ReporterProxy.browser_mob_server.create_proxy(
            params={"trustAllServers": "true", "port": sub_instance_port,
                    "bindAddress": ReporterProxy.get_ip(), 'httpProxy': upstream_chained_proxy})
        Shield34Logger.logger.console(
            "\nStarting new Shield34 Proxy instance on port {} through proxy {}".format(sub_instance_port,
                                                                                        upstream_chained_proxy))
    else:
        proxy = ReporterProxy.browser_mob_server.create_proxy(
            params={"trustAllServers": "true", "port": sub_instance_port,
                    "bindAddress": ReporterProxy.get_ip()})
        Shield34Logger.logger.console("\nStarting new Shield34 Proxy instance on port {}".format(sub_instance_port))

    proxy.base_server = ReporterProxy.browser_mob_server
    create_new_har(proxy)

    return proxy


def create_new_har(proxy):
    har_options = {'captureHeaders': True, 'captureContent': True, 'captureCookies': True,
               'captureBinaryContent': True, 'initialPageRef': True, 'initialPageTitle': True}

    if Shield34Properties.send_data_policy == 'strict':
        har_options = {'captureHeaders': True, 'captureContent': False, 'captureCookies': False,
                   'captureBinaryContent': False, 'initialPageRef': True, 'initialPageTitle': True}

    if Shield34Properties.send_data_policy == 'none':
        har_options = {'captureHeaders': False, 'captureContent': False, 'captureCookies': False,
                   'captureBinaryContent': False, 'initialPageRef': False, 'initialPageTitle': False}

    proxy.new_har("shield34.com", options=har_options)