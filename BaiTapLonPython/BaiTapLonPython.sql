drop table if exists tasks;
drop table if exists users;
drop table if exists categories;
drop type if exists status_enum;


create table categories (
    id serial primary key,
    name varchar(100) not null unique,
    description text
);


create table users (
    id serial primary key,
    full_name varchar(100) not null,
    email varchar(100) unique
);


create table task_status (
    id serial primary key,
    status_name varchar(50) not null unique
);


create type status_enum as enum ('mới', 'đang làm', 'xong', 'tạm dừng');


create table tasks (
    id serial primary key,
    task_name varchar(255) not null,
    category_id integer references categories(id) on delete set null,
    user_id integer references users(id) on delete set null,
    status status_enum default 'mới', -- sử dụng enum ở đây
    priority varchar(20),
    deadline date
);


truncate tasks, users, categories  restart identity;


insert into categories (name, description) values 
('Phát triển Phần mềm', 'Lập trình hệ thống và ứng dụng'),
('Thiết kế & UI/UX', 'Sáng tạo giao diện và đồ họa'),
('Digital Marketing', 'Truyền thông và quảng cáo số'),
('Tài chính - Kế toán', 'Quản lý ngân sách và hóa đơn'),
('Nhân sự & Đào tạo', 'Tuyển dụng và phát triển con người'),
('Hành chính - Vận hành', 'Công việc văn phòng và quy trình nội bộ'),
('Kỹ thuật & Bảo trì', 'Hỗ trợ IT và hạ tầng thiết bị'),
('Quản lý Dự án', 'Điều phối và lập kế hoạch chung');


insert into users (full_name, email) values 
('Nguyễn Văn Nam', 'nam.nv@gmail.com'),
('Trần Thị Tuyết', 'tuyet.tt@gmail.com'),
('Lê Hoàng Anh', 'anh.lh@gmail.com'),
('Phạm Quang Huy', 'huy.pq@gmail.com'),
('Hoàng Thu Thủy', 'thuy.ht@gmail.com'),
('Đỗ Minh Tuấn', 'tuan.dm@gmail.com'),
('Vũ Thị Thanh', 'thanh.vt@gmail.com'),
('Bùi Xuân Hiếu', 'hieu.bx@gmail.com'),
('Đặng Phương Thảo', 'thao.dp@gmail.com'),
('Ngô Quốc Việt', 'viet.nq@gmail.com'),
('Trịnh Minh Tiến', 'tien.tm@gmail.com'),
('Nguyễn Thị Lan', 'lan.nt@gmail.com'),
('Lương Ngọc Diệp', 'diep.ln@gmail.com'),
('Phan Trung Kiên', 'kien.pt@gmail.com'),
('Đào Duy Tùng', 'tung.dd@gmail.com'),
('Trần Hồng Hạnh', 'hanh.th@gmail.com'),
('Lê Ngọc Sơn', 'son.ln@gmail.com'),
('Đoàn Minh Nhật', 'nhat.dm@gmail.com'),
('Nguyễn Tiến Đạt', 'dat.nt@gmail.com'),
('Vũ Đức Thắng', 'thang.vd@gmail.com');

insert into tasks (task_name, category_id, user_id, status, priority, deadline) values 
('Xây dựng API Login', 1, 1, 'đang làm', 'cao', '2026-04-15'),
('Thiết kế poster sự kiện hè', 2, 5, 'mới', 'trung bình', '2026-05-10'),
('Viết kịch bản video TikTok', 3, 2, 'đang làm', 'thấp', '2026-04-12'),
('Rà soát hợp đồng văn phòng', 6, 7, 'xong', 'khẩn cấp', '2026-04-05'),
('Tuyển dụng thực tập sinh', 5, 10, 'mới', 'cao', '2026-05-20'),
('Tối ưu hóa Database', 1, 3, 'đang làm', 'cao', '2026-04-25'),
('Lập báo cáo thuế quý 1', 4, 9, 'tạm dừng', 'khẩn cấp', '2026-04-30'),
('Fix lỗi vỡ layout web', 2, 4, 'đang làm', 'cao', '2026-04-11'),
('Chuẩn bị quà khách hàng', 6, 12, 'mới', 'thấp', '2026-06-01'),
('Backup dữ liệu server', 7, 15, 'xong', 'cao', '2026-04-01'),
('Đào tạo nội bộ về Scrum', 5, 6, 'mới', 'trung bình', '2026-05-15'),
('Kiểm tra chất lượng bản 1.2', 8, 8, 'đang làm', 'khẩn cấp', '2026-04-14'),
('Khảo sát nhân viên', 5, 11, 'mới', 'thấp', '2026-05-05'),
('Phân tích doanh thu tháng 3', 4, 14, 'xong', 'cao', '2026-04-03'),
('Mua sắm laptop mới', 7, 13, 'đang làm', 'cao', '2026-04-20'),
('Cài đặt phòng máy', 7, 16, 'xong', 'trung bình', '2026-04-07'),
('Lên kế hoạch Ads TikTok', 3, 18, 'mới', 'cao', '2026-05-01'),
('Dọn dẹp kho hồ sơ', 6, 17, 'xong', 'thấp', '2026-04-02'),
('Xây dựng hệ thống Firewall', 7, 20, 'đang làm', 'khẩn cấp', '2026-04-22'),
('Dịch tài liệu kỹ thuật', 1, 19, 'mới', 'trung bình', '2026-05-12');