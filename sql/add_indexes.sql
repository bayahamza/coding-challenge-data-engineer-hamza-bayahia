CREATE INDEX IF NOT EXISTS idx_events_user_time ON events(user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_events_product_type ON events(product_id, event_type);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
