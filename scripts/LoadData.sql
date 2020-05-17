SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE 'Comments.csv' INTO TABLE Comments 
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(commentId,authorId,parentPostId,text,dateCreated,readByPoster);

LOAD DATA LOCAL INFILE 'FollowedGroups.csv' INTO TABLE `FollowedGroups`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, groupId, following_date);


LOAD DATA LOCAL INFILE 'FollowedGroupsNotifications.csv' INTO TABLE FollowedGroupsNotifications
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, GroupId, postId, seenByFollower);


LOAD DATA LOCAL INFILE 'FollowedPeople.csv' INTO TABLE FollowedPeople
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, followedUserId, dateCreated);

LOAD DATA LOCAL INFILE 'FollowedPeopleNotifications.csv' INTO TABLE FollowedPeopleNotifications
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, FollowedUserId, postId, seenByFollower);

LOAD DATA LOCAL INFILE 'FollowedTopics.csv' INTO TABLE FollowedTopics
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, TopicId, dateCreated);


LOAD DATA LOCAL INFILE 'FollowedTopicsNotifications.csv' INTO TABLE FollowedTopicsNotifications
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(UserId, FollowedTopicId, postId, seenByFollower);


LOAD DATA LOCAL INFILE 'Friends.csv' INTO TABLE Friends
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id, friend1Id, friend2Id, dateFriended);


LOAD DATA LOCAL INFILE 'GroupMembers.csv' INTO TABLE GroupMembers
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(Userid, Groupid, date_added, addedByUserId);

LOAD DATA LOCAL INFILE 'Groups.csv' INTO TABLE `Groups`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id, name, description, created_date, groupCreatorId, logoImageId);

LOAD DATA LOCAL INFILE 'Location.csv' INTO TABLE `Location`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(locationID, name, description, city, country);

LOAD DATA LOCAL INFILE 'Party.csv' INTO TABLE `Party`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id);

LOAD DATA LOCAL INFILE 'PostIds.csv' INTO TABLE `PostIDs`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(postID);

LOAD DATA LOCAL INFILE 'PostLocations.csv' INTO TABLE `PostLocations`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(PostID, locationID);

LOAD DATA LOCAL INFILE 'PostReactions.csv' INTO TABLE `PostReactions`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(postID, reactorID, ReactionId, dateCreated);

LOAD DATA LOCAL INFILE 'Posts.csv' INTO TABLE `Post`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(postId, authorId, text, datePosted);

LOAD DATA LOCAL INFILE 'PostsTopics.csv' INTO TABLE `PostTopic`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(postId, topicId);

LOAD DATA LOCAL INFILE 'Reactions.csv' INTO TABLE `Reaction`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id, displayName,createdDate, displayIconImageId);

LOAD DATA LOCAL INFILE 'TaggedPeople.csv' INTO TABLE `TaggedPeople`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(postID, userID, seenByUser);

LOAD DATA LOCAL INFILE 'Topic.csv' INTO TABLE `Topic`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id, displayName,topicCreatorId, parentTopicId, description, dateCreated);

LOAD DATA LOCAL INFILE 'User.csv' INTO TABLE `User`
FIELDS TERMINATED BY '|' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES 
(id, first_name, last_name, display_name, email, bio, birthday, avatarImageId);

SET FOREIGN_KEY_CHECKS = 1;