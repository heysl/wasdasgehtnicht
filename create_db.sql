CREATE TABLE wasdasgehtnicht (
    dt_time_unix real primary key,
    dt_time text,
    status_ip4 int(1),
    error_ip4 text,
    status_ip6 int(1),
    error_ip6 text,
    status_dns int(1),
    error_dns text,
    exported int(1)
);