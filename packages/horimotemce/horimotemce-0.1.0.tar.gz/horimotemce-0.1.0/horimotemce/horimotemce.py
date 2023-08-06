"""Bridge MCE IR remote events to a Horimote client."""

import signal
import socket
import logging
import traceback
import time
import random
from threading import Timer
import horimote
from .keys import HORIZON_KEY_MAP

APP_NAME = "horimotemce"
_LOGGER = logging.getLogger(APP_NAME)
_LOG_LEVEL = logging.INFO

LIRC_SOCK_PATH = "/var/run/lirc/lircd"
HORIZON_MEDIA_HOST = "horizon-media"
SOCK_BUFSIZE = 4096
RECONNECT_DELAY_MAX = 64
MIN_REPEAT_TIME_MS = 740
CACHED_EVENT_EXPIRE_TIME = 5
HORIMOTE_KEEPALIVE_TIME = 15.0


class ExitApp(Exception):
    pass


class HorimoteDisconnected(Exception):
    pass


class LircDisconnected(Exception):
    pass


## https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
def set_keepalive(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


class HorimoteClient(horimote.Client):
    """Extended Horimote client that supports keepalive."""

    def __init__(self, ip, port=5900):
        self._keepalive_timer = None
        super().__init__(ip, port)

    def connect(self):
        """Start keepalive timer after successfully connecting."""
        super().connect()
        # self.init_keepalive_timer()
        set_keepalive(self.con, 15, 1, 5)

    def disconnect(self):
        """Disconnect and free socket on disconnect."""
        if self._keepalive_timer:
            _LOGGER.debug("Stopping existing keepalive timer")
            self._keepalive_timer.cancel()
        super().disconnect()
        del self.con

    def send_key(self, key):
        """Start keepalive timer after sending a key."""
        super().send_key(key)
        # self.init_keepalive_timer()

    def init_keepalive_timer(self):
        """Initialise keepalive."""
        if self._keepalive_timer:
            self._keepalive_timer.cancel()
            _LOGGER.debug("Stopped existing keepalive timer")
            del self._keepalive_timer
        self._keepalive_timer = Timer(HORIMOTE_KEEPALIVE_TIME, self.send_keepalive)
        self._keepalive_timer.start()
        _LOGGER.debug(f"Started keepalive timer for {HORIMOTE_KEEPALIVE_TIME}s")

    def send_keepalive(self):
        """Send a keepalive packet."""
        self._keepalive_timer = None
        if self.con != None:
            try:
                _LOGGER.debug(f"Sending keepalive")
                self.con.send(b"")
            except OSError as e:
                _LOGGER.error(f"Could not send to Horizon: {e}")
                raise HorimoteDisconnected
        self.init_keepalive_timer()


class LircClient:
    """Class for lirc socket."""

    ## Save retry event across disconnect/reconnects
    _retry_event = None
    _last_event_time = 0

    def __init__(self, sock_path):
        ## Connect to socket
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.connect(sock_path)
        _LOGGER.info(f"Connected to lirc socket {sock_path}")

    def event_loop(self, horimote_client):
        event = None
        if LircClient._retry_event:
            ## Handle saved event
            event = LircClient._retry_event
            LircClient._retry_event = None
            event_timedelta = round(time.time() - LircClient._last_event_time, 4)
            if event_timedelta >= CACHED_EVENT_EXPIRE_TIME:
                _LOGGER.debug(
                    f"Ignoring saved event: '{event}' (expired: {event_timedelta}s ago)"
                )
                event = None  ## Ignore expired saved event
            else:
                _LOGGER.debug(
                    f"Processing saved event: '{event}' (generated {event_timedelta}s ago)"
                )

        if not event:
            try:
                ## Read a key event from the socket
                event = self._sock.recv(SOCK_BUFSIZE)
                _LOGGER.debug(f"Receive event: '{event}'")
            except OSError as e:
                ## socket error, mark disconnected
                _LOGGER.error(f"Could not read from lirc: {e}")
                raise LircDisconnected

        if event:
            ## Map and send to horimote
            try:
                event_time = time.time()
                event_timedelta_ms = (event_time - LircClient._last_event_time) * 1000
                event_info = str(event).split(" ", 4)

                repeat_flag = event_info[1] != "0"
                if repeat_flag and event_timedelta_ms < MIN_REPEAT_TIME_MS:
                    ## Ignore repeated key
                    return

                LircClient._last_event_time = event_time
                mce_key = event_info[2]
                horizon_key = HORIZON_KEY_MAP.get(mce_key)
                _LOGGER.debug(
                    f"Map key: {mce_key} to: {str(horizon_key)} (+{round(event_timedelta_ms)}ms)"
                )
                if horizon_key:
                    horimote_client.send_key(horizon_key)
                else:
                    _LOGGER.debug(f"Ignoring unmapped key: {mce_key}")
            except OSError as e:
                _LOGGER.error(f"Could not send to Horizon: {e}")
                LircClient._retry_event = bytes(
                    event
                )  ## Save event to replay when connected
                raise HorimoteDisconnected
        else:
            ## Socket disconnected
            _LOGGER.error(f"Empty event received from lirc")
            raise LircDisconnected

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        _LOGGER.debug("Disconnected from lirc socket")
        self._sock.close()


def get_backoff_delay(retry_count):
    """Calculate exponential backoff with random jitter delay."""
    delay = round(
        min(RECONNECT_DELAY_MAX, (2 ** retry_count) - 1)
        + (random.randint(0, 1000) / 1000),
        4,
    )
    return delay


def main_loop():
    ## Create horimote client
    host = HORIZON_MEDIA_HOST
    lirc_sock_path = LIRC_SOCK_PATH
    horimote_retry = 0
    while True:
        try:
            _LOGGER.debug(f"Connecting to Horizon host {host}")
            with HorimoteClient(host) as horimote_client:
                _LOGGER.info(f"Connected to Horizon host {host}")
                horimote_retry = 0
                lirc_retry = 0
                while True:
                    try:
                        ## Open lirc socket
                        with LircClient(lirc_sock_path) as lirc_client:
                            lirc_retry = 0
                            while True:
                                ## Process events
                                lirc_client.event_loop(horimote_client)
                    except OSError as e:
                        if lirc_retry == 0:
                            _LOGGER.error(f"Could not connect to lirc: {e}")
                        else:
                            _LOGGER.debug(f"Retry #{lirc_retry} failed: {e}")
                    except LircDisconnected:
                        pass
                    except HorimoteDisconnected:
                        break

                    ## Reconnect lirc client if horimote still connected
                    lirc_delay = get_backoff_delay(lirc_retry)
                    _LOGGER.debug(f"Waiting {lirc_delay}s before retrying lirc")
                    time.sleep(lirc_delay)
                    lirc_retry += 1

        except OSError as e:
            if horimote_retry == 0:
                _LOGGER.error(f"Could not connect to Horizon host: {e}")
            else:
                _LOGGER.debug(f"Retry #{horimote_retry} failed: {e}")
        # except Exception as e:
        #     _LOGGER.error(f'Exception: {e}')
        #     traceback.print_exc()

        ## Delay reconnection to horimote
        horimote_delay = get_backoff_delay(horimote_retry)
        _LOGGER.debug(f"Waiting {horimote_delay}s before retrying Horizon")
        time.sleep(horimote_delay)
        horimote_retry += 1


def sigterm_handler(signal, frame):
    _LOGGER.warning("SIGTERM received, exiting")
    raise ExitApp


def main():
    try:
        ## Catch SIGTERM and enable logging
        logging.basicConfig(
            level=_LOG_LEVEL,
            format="%(asctime)s %(levelname)s[%(threadName)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        signal.signal(signal.SIGTERM, sigterm_handler)

        ## Start main loop
        main_loop()
    except KeyboardInterrupt:
        _LOGGER.warning("Keyboard interrupt, exiting")
        exit(255)
    except ExitApp:
        exit(0)
    except Exception as e:
        _LOGGER.error(f"Exception: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()