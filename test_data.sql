-- Вставка новых данных в таблицу employee
INSERT INTO employee (id, username, first_name, last_name, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-446655440010', 'Kirill', 'Kirill', 'Zlobin', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440011', 'Test_user_1', 'Kirill', 'Zlobin', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440012', 'Test_user_2', 'Kirill', 'Zlobin', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440013', 'Vozmite_Na_stajirovku', 'Kirill', 'Zlobin', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440014', 'Plz', 'Kirill', 'Zlobin', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440015', 'Meow', 'Kirill', 'Zlobin', NOW(), NOW());



-- Вставка новых данных в таблицу organization
INSERT INTO organization (id, name, description, type, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'Avito', 'A leading tech company.', 'IE', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440002', 'Yandex', 'A leading tech company.', 'LLC', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440005', 'Kirill_Org', 'A leading tech company.', 'JSC', NOW(), NOW());



-- Вставка новых данных в таблицу organization_responsible
INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-446655440055', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440010'),
    ('550e8400-e29b-41d4-a716-446655440056', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440011'),
    ('550e8400-e29b-41d4-a716-446655440023', '550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440012'),
    ('550e8400-e29b-41d4-a716-446655440024', '550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440013'),
    ('550e8400-e29b-41d4-a716-446655440025', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440014');


INSERT INTO tenders (id, name, description, status, service_type, version, organization_id, creator_username, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-446655440020', 'Tender for Tech Services', 'A tender for various tech services', 'Created', 'Delivery', 1, '550e8400-e29b-41d4-a716-446655440000', 'Kirill', NOW(), NOW());