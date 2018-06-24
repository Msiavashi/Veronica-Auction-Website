$TTL 86400
$ORIGIN bordito.com.

@ IN SOA ns1.bordito.com. info.bordito.com. (
        2018032701 ; serial
        3600    ; refresh
        1800    ; retry
        604800  ; expire
        86400   ; Minimum TTL
)

  IN  NS ns1.bordito.com.
  IN  NS ns2.bordito.com.
  IN  A  89.42.209.140
ns1 IN A 89.42.209.140
ns2 IN A 89.42.209.140
www.bordito.com. IN A 89.42.209.140
ftp.bordito.com. IN A 89.42.209.140
mail.bordito.com. IN A 89.42.209.140
  IN MX 10 mail.bordito.com.
