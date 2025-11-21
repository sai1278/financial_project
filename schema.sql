CREATE TABLE financials (
  id INT AUTO_INCREMENT PRIMARY KEY,
  company_id VARCHAR(50),
  revenue FLOAT,
  profit FLOAT,
  pe_ratio FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
