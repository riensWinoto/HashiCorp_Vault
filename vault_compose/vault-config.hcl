disable_mlock = true
ui = true

listener "tcp" {
    tls_disable = 1
    address = "[::]:8200"
    cluster_address = "[::]:8201"
}
storage "postgresql" {
    enable_ha = "true"
    connection_url = "postgresurl"
    table = "vault_kv_store"
    ha_table = "vault_ha_locks"
    max_parallel = "10"
}
