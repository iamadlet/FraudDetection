-- Fraud Detection Database Schema
-- Run this script to create the necessary tables

CREATE TABLE IF NOT EXISTS validated_transactions (
    id SERIAL PRIMARY KEY,
    cst_dim_id VARCHAR(50) NOT NULL,
    transdate DATE NOT NULL,
    transdatetime TIMESTAMP NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    docno VARCHAR(50) NOT NULL,
    direction VARCHAR(20) NOT NULL,
    target INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patterns (
    id SERIAL PRIMARY KEY,
    transdate DATE NOT NULL,
    cst_dim_id VARCHAR(50) NOT NULL,
    monthly_os_changes INTEGER NOT NULL,
    monthly_phone_model_changes INTEGER NOT NULL,
    last_phone_model_categorical VARCHAR(100),
    last_os_categorical VARCHAR(100),
    logins_last_7_days INTEGER NOT NULL,
    logins_last_30_days INTEGER NOT NULL,
    login_frequency_7d NUMERIC(10, 4) NOT NULL,
    login_frequency_30d NUMERIC(10, 4) NOT NULL,
    freq_change_7d_vs_mean NUMERIC(10, 4) NOT NULL,
    logins_7d_over_30d_ratio NUMERIC(10, 4) NOT NULL,
    avg_login_interval_30d NUMERIC(10, 4) NOT NULL,
    std_login_interval_30d NUMERIC(10, 4) NOT NULL,
    var_login_interval_30d NUMERIC(10, 4) NOT NULL,
    ewm_login_interval_7d NUMERIC(10, 4) NOT NULL,
    burstiness_login_interval NUMERIC(10, 4) NOT NULL,
    fano_factor_login_interval NUMERIC(10, 4) NOT NULL,
    zscore_avg_login_interval_7d NUMERIC(10, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_validated_transactions_cst_dim_id ON validated_transactions(cst_dim_id);
CREATE INDEX idx_validated_transactions_transdate ON validated_transactions(transdate);
CREATE INDEX idx_patterns_cst_dim_id ON patterns(cst_dim_id);
CREATE INDEX idx_patterns_transdate ON patterns(transdate);
