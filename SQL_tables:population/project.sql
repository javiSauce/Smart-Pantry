create schema smartpantry;
set search_path ='smartpantry';

create domain id as numeric(10);
create domain location as varchar(40);



create table admin(
admin_id 		id		not null,
name		varchar(30)		not null,
dob		date		not null check (dob between date '1900-01-01' and date'1999-01-01'),
email	varchar(320)	not null 	unique,
country 	location,
primary key(admin_id)
);

create table ingredient (
ingr_id 				id 		not null,
name			varchar(30)		not null,
count			smallint,
price_per_item	money,
threshold		smallint,
date 			date		default now(),
primary key(ingr_id)
);

create table pantry (
pantry_id 		id 		not null,
adminid			id		not null,
temperature 	numeric(5)	not null,
date		date	not null,
time		time with time zone	not null, 
primary key(pantry_id),
foreign key(adminid) references admin(admin_id) on delete restrict
on update cascade
);


create table meal(
meal_id 		id 			not null,	
name		varchar(300) 	not null,
description 	text,
primary key(meal_id)

);

create table chef(
chef_id 		id		not null,
name		varchar(30)	not null,
dob		date,
email	varchar(320)	not null unique,
country		location,
primary key(chef_id)
);

create table regular_user(
reg_id 		id		not null,
name		varchar(30),
dob		date		not null,
email	varchar(320) not null unique,
country		location not null,
primary key(reg_id)

);

create table meal_order(
order_id 		id		not null,
creator_id 		id		not null,
meal_id			id 		not null,
count			integer,	
state			boolean,
primary key(order_id),
foreign key(creator_id) references regular_user(reg_id),
foreign key(meal_id) references meal(meal_id) 
);

create table ingr_order(
order_id		id 		not null,
creator_id		id		not null,
ingr_id			id 		not null,
count			integer,
primary key(order_id),
foreign key(creator_id) references chef(chef_id),
foreign key(ingr_id) references ingredient(ingr_id)
);

create table report (
report_id		id				not null,
name			varchar(120),
description 	text,
primary key(report_id)
);

--relations

create table orders(
id 		id,
order_id	id,
foreign key(id) references admin(admin_id),
foreign key(order_id) references ingr_order(order_id)
);

create table access(
chef_id 	id,
report_id	id,
admin_id	id,
foreign key(chef_id) references chef(chef_id),
foreign key(report_id) references report(report_id),
foreign key(admin_id) references admin(admin_id)
);

create table creates(
meal_id id,
chef_id	id,
foreign key(meal_id) references meal(meal_id),
foreign key(chef_id) references chef(chef_id)
);

create table reviews(
order_id	id,
admin_id id,
foreign key(order_id) references meal_order(order_id),
foreign key(admin_id) references admin(admin_id)
);


create table requests(
chef_id id,
order_id id,
pantry_id id,
reg_id id,
foreign key(reg_id) references regular_user(reg_id),
foreign key(order_id) references ingr_order(order_id),
foreign key(chef_id) references chef(chef_id),
foreign key(pantry_id) references pantry(pantry_id)
);


create table meals(
meal_id id,
ingr_id id,
quantity integer,
foreign key (meal_id) references meal(meal_id),
foreign key (ingr_id) references ingredient(ingr_id));