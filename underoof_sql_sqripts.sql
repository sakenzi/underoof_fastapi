TRUNCATE TABLE 
    advertisement_photos,
    advertisements,
    type_advertisements,
    photos,
    locations,
    user_roles,
    roles,
    phone_codes,
    user_roles
RESTART IDENTITY CASCADE;

INSERT INTO users (first_name, last_name, surname, email, phone_number, password, verification_code, is_active)
VALUES
('Айдос', 'Нуртаев', 'Касымович', 'aidos1@example.com', '+77010000001', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '123456', TRUE),
('Мария', 'Иванова', 'Петровна', 'maria2@example.com', '+77010000002', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '654321', TRUE),
('Данияр', 'Смагулов', 'Ержанович', 'daniyar3@example.com', '+77010000003', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '111111', TRUE),
('Елена', 'Корнилова', 'Алексеевна', 'elena4@example.com', '+77010000004', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '222222', FALSE),
('Жанна', 'Тлеубаева', 'Маратовна', 'zhanna5@example.com', '+77010000005', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '333333', TRUE),
('Алексей', 'Федоров', 'Сергеевич', 'alex6@example.com', '+77010000006', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '444444', TRUE),
('Ирина', 'Кузнецова', 'Владимировна', 'irina7@example.com', '+77010000007', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '555555', FALSE),
('Олег', 'Токтаров', 'Бакытович', 'oleg8@example.com', '+77010000008', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '666666', TRUE),
('Надежда', 'Серикбаева', 'Жаксылыковна', 'nadezhda9@example.com', '+77010000009', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '777777', TRUE),
('Павел', 'Акимов', 'Геннадьевич', 'pavel10@example.com', '+77010000010', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '888888', FALSE),
('Аслан', 'Жуматаев', 'Нургалиевич', 'aslan11@example.com', '+77010000011', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '999999', TRUE),
('Виктория', 'Савельева', 'Олеговна', 'vika12@example.com', '+77010000012', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '112233', TRUE),
('Максим', 'Дмитриев', 'Иванович', 'max13@example.com', '+77010000013', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '445566', FALSE),
('Ксения', 'Орлова', 'Станиславовна', 'ksenia14@example.com', '+77010000014', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '778899', TRUE),
('Рустам', 'Алиев', 'Фаридович', 'rustam15@example.com', '+77010000015', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '889900', TRUE),
('Айгерим', 'Мустафина', 'Нурлановна', 'aigerim16@example.com', '+77010000016', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '990011', FALSE),
('Георгий', 'Семенов', 'Львович', 'georgiy17@example.com', '+77010000017', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '220011', TRUE),
('Светлана', 'Зайцева', 'Андреевна', 'sveta18@example.com', '+77010000018', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '334455', TRUE),
('Ермек', 'Аманов', 'Жумагалиевич', 'ermek19@example.com', '+77010000019', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '667788', FALSE),
('Алиса', 'Попова', 'Викторовна', 'alisa20@example.com', '+77010000020', '9cdcfbbe0183b2f1855ee2f7354fb2a8d175b133b227052a095302b4559bf525', '889977', TRUE);

INSERT INTO phone_codes (phone_number, code, is_verified)
VALUES
('+77010000001', '1111', TRUE),
('+77010000002', '2222', TRUE),
('+77010000003', '3333', FALSE),
('+77010000004', '4444', TRUE),
('+77010000005', '5555', FALSE),
('+77010000006', '6666', TRUE),
('+77010000007', '7777', TRUE),
('+77010000008', '8888', FALSE),
('+77010000009', '9999', TRUE),
('+77010000010', '1010', TRUE),
('+77010000011', '1112', TRUE),
('+77010000012', '1212', FALSE),
('+77010000013', '1313', TRUE),
('+77010000014', '1414', TRUE),
('+77010000015', '1515', FALSE),
('+77010000016', '1616', TRUE),
('+77010000017', '1717', TRUE),
('+77010000018', '1818', FALSE),
('+77010000019', '1919', TRUE),
('+77010000020', '2020', TRUE);


INSERT INTO roles (role_name)
VALUES
('Арендатель'),
('Продавец');

INSERT INTO user_roles (user_id, role_id)
VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 2),
(12, 2),
(13, 2),
(14, 2),
(15, 2),
(16, 2),
(17, 2),
(18, 2),
(19, 2),
(20, 2);


INSERT INTO public.locations (id, "number", latitude, longitude, geom, street_id) VALUES
(1, '28', 49.770548, 73.126189, '0101000020E61000005B07077B13485240C5FF1D51A1E24840', 1),
(2, '17/2', 49.762682, 73.159974, '0101000020E6100000768D96033D4A5240BA9F53909FE14840', 2),
(3, '37', 49.808105, 73.082537, '0101000020E610000070ED444948455240F65D11FC6FE74840', 3),
(4, '29', 49.811088, 73.081650, '0101000020E6100000FAEDEBC039455240CA1649BBD1E74840', 3),
(5, '33/2', 49.795680, 73.079174, '0101000020E6100000622CD32F11455240670A9DD7D8E54840', 4),
(6, '53/1', 49.801263, 73.083060, '0101000020E6100000C5E6E3DA50455240573F36C98FE64840', 5),
(7, '1В', 49.789330, 73.105451, '0101000020E610000027158DB5BF46524037E0F3C308E54840', 6),
(8, '12а', 49.806677, 73.060023, '0101000020E61000008080B56AD7435240BBB7223141E74840', 7),
(9, '5', 49.790053, 73.099598, '0101000020E6100000CF2F4AD05F465240A88DEA7420E54840', 8),
(10, '1/2', 49.879590, 73.182253, '0101000020E610000044A67C08AA4B5240BFF1B56796F04840', 9),
(11, '25', 49.775698, 73.138003, '0101000020E6100000FEEF880AD54852404BC972124AE34840', 10),
(12, '49/1', 49.809795, 73.103368, '0101000020E6100000FDDCD0949D4652406FBBD05CA7E74840', 11),
(13, '22', 49.771935, 73.144852, '0101000020E6100000A7B0524145495240A2D11DC4CEE24840', 12);


INSERT INTO photos (photo_link)
VALUES
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFe8f5JB8P1kO0UfoNvCmpFu6_tJednvKwlA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr3fWlJ8MpOS4ttBrPTrv84HdHrG9Sb66C6A&s'),
('https://hips.hearstapps.com/hmg-prod/images/hbx010124amandajacobs-005-66e05129caa45.jpg?crop=1xw:0.84375xh;0,0.197xh'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO_b-YTwImwx9xjkL6YE5MMK1rxqNgkC1_7Q&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcpz8y-OFUUEs_2sDcWRyyv8yaO7F_vAyvbA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFe8f5JB8P1kO0UfoNvCmpFu6_tJednvKwlA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr3fWlJ8MpOS4ttBrPTrv84HdHrG9Sb66C6A&s'),
('https://hips.hearstapps.com/hmg-prod/images/hbx010124amandajacobs-005-66e05129caa45.jpg?crop=1xw:0.84375xh;0,0.197xh'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO_b-YTwImwx9xjkL6YE5MMK1rxqNgkC1_7Q&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcpz8y-OFUUEs_2sDcWRyyv8yaO7F_vAyvbA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFe8f5JB8P1kO0UfoNvCmpFu6_tJednvKwlA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr3fWlJ8MpOS4ttBrPTrv84HdHrG9Sb66C6A&s'),
('https://hips.hearstapps.com/hmg-prod/images/hbx010124amandajacobs-005-66e05129caa45.jpg?crop=1xw:0.84375xh;0,0.197xh'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO_b-YTwImwx9xjkL6YE5MMK1rxqNgkC1_7Q&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcpz8y-OFUUEs_2sDcWRyyv8yaO7F_vAyvbA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFe8f5JB8P1kO0UfoNvCmpFu6_tJednvKwlA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr3fWlJ8MpOS4ttBrPTrv84HdHrG9Sb66C6A&s'),
('https://hips.hearstapps.com/hmg-prod/images/hbx010124amandajacobs-005-66e05129caa45.jpg?crop=1xw:0.84375xh;0,0.197xh'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO_b-YTwImwx9xjkL6YE5MMK1rxqNgkC1_7Q&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcpz8y-OFUUEs_2sDcWRyyv8yaO7F_vAyvbA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFe8f5JB8P1kO0UfoNvCmpFu6_tJednvKwlA&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr3fWlJ8MpOS4ttBrPTrv84HdHrG9Sb66C6A&s'),
('https://hips.hearstapps.com/hmg-prod/images/hbx010124amandajacobs-005-66e05129caa45.jpg?crop=1xw:0.84375xh;0,0.197xh'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO_b-YTwImwx9xjkL6YE5MMK1rxqNgkC1_7Q&s'),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcpz8y-OFUUEs_2sDcWRyyv8yaO7F_vAyvbA&s');


INSERT INTO type_advertisements (type_name)
VALUES
('Аренда квартиры'),
('Продажа квартиры'),
('Аренда дома'),
('Продажа дома'),
('Комната в аренду'),
('Посуточная аренда'),
('Коммерческая недвижимость'),
('Продажа участка'),
('Аренда офиса'),
('Продажа офиса'),
('Аренда магазина'),
('Продажа магазина'),
('Аренда склада'),
('Продажа склада'),
('Аренда гаража'),
('Продажа гаража'),
('Элитная недвижимость'),
('Загородный дом'),
('Дача'),
('Апартаменты');



INSERT INTO advertisements (description, number_of_room, quadrature, floor, price, from_the_date, before_the_date, is_active, location_id, type_advertisement_id, user_role_id)
VALUES
('Сдаётся уютная квартира', 2, 45.5, 3, 120000, '2025-01-01', '2025-12-31', TRUE, 1, 1, 1),
('Продаётся квартира в центре', 3, 78.0, 5, 35000000, '2025-02-01', '2025-12-31', TRUE, 2, 2, 2),
('Дом в аренду на долгий срок', 4, 120.0, 2, 250000, '2025-01-15', '2025-11-30', TRUE, 3, 3, 3),
('Продажа просторного дома', 5, 200.0, 2, 75000000, '2025-03-01', '2025-12-31', TRUE, 4, 4, 4),
('Комната в аренду студентам', 1, 18.0, 4, 50000, '2025-01-05', '2025-06-30', TRUE, 5, 5, 5),
('Посуточная аренда квартиры', 2, 55.0, 7, 15000, '2025-01-01', '2025-12-31', TRUE, 6, 6, 6),
('Коммерческое помещение в аренду', NULL, 90.0, 1, 300000, '2025-01-20', '2025-12-31', TRUE, 7, 7, 7),
('Продажа земельного участка', NULL, 600.0, NULL, 12000000, '2025-02-01', '2025-12-31', TRUE, 8, 8, 8),
('Офис в аренду в бизнес-центре', NULL, 40.0, 10, 200000, '2025-01-10', '2025-11-30', TRUE, 9, 9, 9),
('Продажа офиса', NULL, 70.0, 2, 25000000, '2025-01-15', '2025-12-31', TRUE, 10, 10, 10),
('Аренда магазина на рынке', NULL, 30.0, 1, 180000, '2025-01-01', '2025-12-31', TRUE, 11, 11, 11),
('Продажа магазина в ТРЦ', NULL, 85.0, 1, 60000000, '2025-02-01', '2025-12-31', TRUE, 12, 12, 12),
('Аренда склада', NULL, 200.0, NULL, 400000, '2025-03-01', '2025-12-31', TRUE, 13, 13, 13);


INSERT INTO advertisement_photos (photo_id, advertisement_id)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13);
