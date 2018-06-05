beacons:
  nagiosOutput:
    - icmp_check:
        command: "check_icmp"
        params: 8.8.8.8
        threshold: 0
        interval: 60
    - dns_check:
        command: "check_dns"
        params: 8.8.8.8
        threshold: 0
        interval: 5
    - http_check:
        command: "check_http"
        params: localhost
        threshold: 2
        interval: 20
    - check_ide:
        command: "check_ide_smart"
        params: "/dev/snapshot"
        threshold: 2
        interval: 20
    - mailq_check:
        command: "check_mailq"
        params: "-H localhost"
        threshold: 2
        interval: 5
    - uptime_check:
        command: "check_uptime"
        params: ""
        threshold: 0
        interval: 5

