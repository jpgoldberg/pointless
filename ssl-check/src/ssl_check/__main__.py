import concurrent.futures

from _check_ssl import CertChecker

HOSTS = [
    ("damjan.softver.org.mk", 443),
    ("expired.badssl.com", 443),
    ("wrong.host.badssl.com", 443),
    ("ca.ocsr.nl", 443),
    ("faß.de", 443),
    ("самодеј.мкд", 443),
]

FEWER_HOSTS = [
    ("jeffrey.goldmark.org",443),
    ("faß.de", 443),
    ("expired.badssl.com", 443),
    ("wrong.host.badssl.com", 443),
    ("does.not.exist.goldmark.org", 443),
    ]


def main():
    checker = CertChecker()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        for hostinfo in e.map(lambda x: checker.get_certificate(x[0], x[1]), FEWER_HOSTS):
            print(hostinfo.basic_info())



if __name__ == "__main__":
    main()