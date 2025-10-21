CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Sarah', 'Johnson', 'sarah.j@email.com', 'Coffee enthusiast and book lover', 'sarahj', 'hashed_password_123', 'https://example.com/images/sarah.jpg', '2024-01-15', 1);

INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Michael', 'Chen', 'mchen@email.com', 'Software developer by day, gamer by night', 'mikec', 'hashed_password_456', 'https://example.com/images/mike.jpg', '2024-02-20', 1);

INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Emma', 'Rodriguez', 'emma.r@email.com', 'Travel photographer exploring the world', 'emmar', 'hashed_password_789', 'https://example.com/images/emma.jpg', '2024-03-10', 1);

INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('James', 'Taylor', 'jtaylor@email.com', 'Fitness coach and nutrition expert', 'jamest', 'hashed_password_321', 'https://example.com/images/james.jpg', '2023-12-05', 0);

INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Priya', 'Patel', 'priya.p@email.com', 'Marketing professional and pet parent', 'priyap', 'hashed_password_654', 'https://example.com/images/priya.jpg', '2024-04-18', 1);

INSERT INTO "Posts" (user_id, category_id, title, publication_date, image_url, content, approved)
VALUES (3, 1, 'Exploring the Mountains', '2024-05-01', 'https://example.com/images/mountains.jpg', 'A thrilling adventure through the rocky terrains.', 1);