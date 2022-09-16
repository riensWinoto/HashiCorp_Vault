storage "file" {
  path = "/etc/vault.d/vault-data"
}

listener "tcp" {
  address       = "yourIP:8282"
  tls_disable = 1
}

api_addr = "http://yourIP:8282"
cluster_addr = "http://yourIP:8283"
ui = true
