INSERT INTO employee (id, username, first_name, last_name, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-446655440000235', 'user1', 'John', 'Doe', NOW(), NOW());
INSERT INTO employee (id, username, first_name, last_name, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-44665544023523', 'user1', 'John', 'Doe', NOW(), NOW());
INSERT INTO employee (id, username, first_name, last_name, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-4466554434643', 'user2', 'John', 'Doe', NOW(), NOW());




INSERT INTO organization (id, name, description, type, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-4466554434634', 'Org 1', 'A leading tech company.', 'LLC', now(), now());
INSERT INTO organization (id, name, description, type, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-446655444574', 'Org 2', 'A leading tech company.', 'IE', now(), now());
INSERT INTO organization (id, name, description, type, created_at, updated_at)
VALUES
    ('550e8400-e29b-41d4-a716-4466554456865', 'Org 3', 'A leading tech company.', 'JSC', now(), now());


INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-446655448678', '550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440001');
INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-44665544876867', '550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440002');
INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-4466554487686', '550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440003');
INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-44665544867', '550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440004');
INSERT INTO organization_responsible (id, organization_id, user_id)
VALUES
    ('550e8400-e29b-41d4-a716-446655448768', '550e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655440005');
