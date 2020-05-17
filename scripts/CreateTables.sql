CREATE TABLE Comments (
  commentID    varchar(40) NOT NULL, 
  authorID     varchar(40) NOT NULL, 
  parentPostID varchar(40) NOT NULL, 
  text         varchar(400), 
  dateCreated  datetime NULL, 
  readByPoster tinyint, 
  PRIMARY KEY (commentID));
CREATE TABLE FollowedGroups (
  Userid         varchar(40) NOT NULL, 
  Groupid        varchar(40) NOT NULL, 
  following_date datetime NULL, 
  PRIMARY KEY (Userid, 
  Groupid));
CREATE TABLE FollowedGroupsNotifications (
  Userid         varchar(40) NOT NULL, 
  Groupid        varchar(40) NOT NULL, 
  postID         varchar(40), 
  seenByFollower tinyint,
  PRIMARY KEY (Userid, Groupid, postID));
CREATE TABLE FollowedPeople (
  Userid         varchar(40) NOT NULL, 
  followedUserId varchar(40) NOT NULL, 
  dateCreated    datetime NULL, 
  PRIMARY KEY (Userid, 
  followedUserId));
CREATE TABLE FollowedPeopleNotifications (
  Userid         varchar(40) NOT NULL, 
  followedUserId varchar(40) NOT NULL, 
  postID         varchar(40), 
  seenByFollower tinyint,
  PRIMARY KEY (Userid, followedUserId, postID));
CREATE TABLE FollowedTopics (
  Userid      varchar(40) NOT NULL, 
  Topicid     varchar(40) NOT NULL, 
  dateCreated datetime NULL, 
  PRIMARY KEY (Userid, 
  Topicid));
CREATE TABLE FollowedTopicsNotifications (
  Userid          varchar(40) NOT NULL, 
  FollowedTopicId varchar(40) NOT NULL, 
  postID          varchar(40), 
  seenByFollower  tinyint,
  PRIMARY KEY (Userid, FollowedTopicId, postID));
CREATE TABLE Friends (
  id            varchar(40) NOT NULL, 
  friend1Id     varchar(40) NOT NULL, 
  friend2Id     varchar(40) NOT NULL, 
  dateFriended  datetime NULL, 
  statusPending tinyint DEFAULT 1, 
  PRIMARY KEY (id));

CREATE TABLE GroupMembers (
  Userid        varchar(40) NOT NULL, 
  Groupid       varchar(40) NOT NULL, 
  date_added    datetime NULL, 
  addedByUserId varchar(40) DEFAULT NULL, 
  PRIMARY KEY (Userid, 
  Groupid));
  
CREATE TABLE `Groups` (
  id             varchar(40) NOT NULL, 
  name           varchar(40), 
  description    varchar(200), 
  created_date   datetime NULL, 
  groupCreatorId varchar(40) NOT NULL, 
  logoImageId    varchar(40) DEFAULT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Image (
  id           varchar(40) NOT NULL, 
  imagePath    varchar(200), 
  dateUploaded datetime NULL, 
  `size`       int(32), 
  PRIMARY KEY (id));
CREATE TABLE Location (
  locationID  varchar(40) NOT NULL, 
  name        varchar(40), 
  description varchar(200), 
  city        varchar(100), 
  country     varchar(50), 
  PRIMARY KEY (locationID));
CREATE TABLE Party (
  id varchar(40) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Post (
  postID     varchar(40) NOT NULL, 
  authorID   varchar(40) NOT NULL, 
  text       varchar(400), 
  datePosted datetime NULL, 
  PRIMARY KEY (postID));
CREATE TABLE Post_Image (
  postID  varchar(40) NOT NULL, 
  ImageId varchar(40) NOT NULL, 
  PRIMARY KEY (postID, 
  ImageId));
CREATE TABLE PostIDs (
  postID varchar(40) NOT NULL, 
  PRIMARY KEY (postID));
CREATE TABLE PostLocations (
  PostID     varchar(40) NOT NULL, 
  locationID varchar(40) NOT NULL, 
  PRIMARY KEY (PostID, 
  locationID));
CREATE TABLE PostReactions (
  postID      varchar(40) NOT NULL, 
  reactorID   varchar(40) NOT NULL, 
  ReactionId  varchar(40) NOT NULL, 
  dateCreated datetime NULL, 
  seenByUser  tinyint, 
  PRIMARY KEY (postID, 
  reactorID, 
  ReactionId));
CREATE TABLE PostTopic (
  postID  varchar(40) NOT NULL, 
  topicid varchar(40) NOT NULL, 
  PRIMARY KEY (postID, 
  topicid));
CREATE TABLE Reaction (
  id                 varchar(40) NOT NULL, 
  displayName        varchar(40), 
  createdDate        datetime NULL, 
  displayIconImageId varchar(40) DEFAULT NULL, 
  PRIMARY KEY (id));
CREATE TABLE TaggedGroups (
  Groupid     varchar(40) NOT NULL, 
  PostID      varchar(40) NOT NULL, 
  seenByGroup tinyint, 
  PRIMARY KEY (Groupid, 
  PostID));
CREATE TABLE TaggedPeople (
  postID     varchar(40) NOT NULL, 
  userID     varchar(40) NOT NULL, 
  seenByUser tinyint, 
  PRIMARY KEY (postID, 
  userID));
CREATE TABLE Topic (
  id             varchar(40) NOT NULL, 
  displayName    varchar(40), 
  parentTopicID  varchar(40) DEFAULT NULL, 
  topicCreatorId varchar(40) NOT NULL, 
  description    varchar(200), 
  dateCreated    datetime NULL, 
  PRIMARY KEY (id));
CREATE TABLE `User` (
  id            varchar(40) NOT NULL, 
  first_name    varchar(20), 
  last_name     varchar(20), 
  display_name  varchar(40), 
  email         varchar(40), 
  bio           varchar(40), 
  birthday      date NULL, 
  avatarImageId varchar(40) DEFAULT NULL, 
  PRIMARY KEY (id));
CREATE TABLE UserMiddleName (
  id           varchar(40) NOT NULL, 
  namePosition int(11) NOT NULL, 
  nameValue    varchar(40) NOT NULL, 
  PRIMARY KEY (id, 
  namePosition));
CREATE TABLE GroupsAdmins (
  Userid  varchar(40) NOT NULL, 
  GroupId varchar(40) NOT NULL, 
  PRIMARY KEY (Userid, 
  GroupId));
CREATE TABLE MembershipRequests (
  UserId      varchar(40) NOT NULL, 
  Groupid     varchar(40) NOT NULL, 
  create_date datetime NULL, 
  PRIMARY KEY (UserId, 
  Groupid)); 
  
ALTER TABLE FollowedGroupsNotifications ADD CONSTRAINT FKFollowedGr880088 FOREIGN KEY (Userid, Groupid) REFERENCES FollowedGroups (Userid, Groupid) ON DELETE CASCADE;
ALTER TABLE FollowedTopicsNotifications ADD CONSTRAINT FKFollowedTo551930 FOREIGN KEY (Userid, FollowedTopicId) REFERENCES FollowedTopics (Userid, Topicid)  ON DELETE CASCADE;
ALTER TABLE FollowedPeopleNotifications ADD CONSTRAINT FKFollowedPe871531 FOREIGN KEY (Userid, followedUserId) REFERENCES FollowedPeople (Userid, followedUserId)  ON DELETE CASCADE;
ALTER TABLE UserMiddleName ADD CONSTRAINT FKUserMiddle59963 FOREIGN KEY (id) REFERENCES `User` (id)  ON DELETE CASCADE;
ALTER TABLE Topic ADD CONSTRAINT FKTopic376226 FOREIGN KEY (topicCreatorId) REFERENCES Party (id)  ON DELETE CASCADE;
ALTER TABLE Post ADD CONSTRAINT FKPost455791 FOREIGN KEY (authorID) REFERENCES Party (id)  ON DELETE CASCADE;
ALTER TABLE Comments ADD CONSTRAINT FKComments190119 FOREIGN KEY (authorID) REFERENCES Party (id) ON DELETE CASCADE;
ALTER TABLE `Groups` ADD CONSTRAINT FKGroups704044 FOREIGN KEY (id) REFERENCES Party (id) ON DELETE CASCADE;
ALTER TABLE `User` ADD CONSTRAINT FKUser537462 FOREIGN KEY (id) REFERENCES Party (id) ON DELETE CASCADE;
ALTER TABLE Post_Image ADD CONSTRAINT FKPost_Image311418 FOREIGN KEY (ImageId) REFERENCES Image (id) ON DELETE CASCADE;
ALTER TABLE Post_Image ADD CONSTRAINT FKPost_Image865939 FOREIGN KEY (postID) REFERENCES Post (postID) ON DELETE CASCADE;
ALTER TABLE `Groups` ADD CONSTRAINT FKGroups422142 FOREIGN KEY (logoImageId) REFERENCES Image (id) ON DELETE CASCADE;
ALTER TABLE TaggedGroups ADD CONSTRAINT FKTaggedGrou851772 FOREIGN KEY (PostID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE TaggedGroups ADD CONSTRAINT FKTaggedGrou740733 FOREIGN KEY (Groupid) REFERENCES `Groups` (id) ON DELETE CASCADE;
ALTER TABLE `Groups` ADD CONSTRAINT FKGroups266239 FOREIGN KEY (groupCreatorId) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE GroupMembers ADD CONSTRAINT FKGroupMembe741011 FOREIGN KEY (Userid) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE FollowedGroups ADD CONSTRAINT FKFollowedGr680437 FOREIGN KEY (Groupid) REFERENCES `Groups` (id) ON DELETE CASCADE;
ALTER TABLE FollowedGroups ADD CONSTRAINT FKFollowedGr327001 FOREIGN KEY (Userid) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE Reaction ADD CONSTRAINT FKReaction576329 FOREIGN KEY (displayIconImageId) REFERENCES Image (id) ON DELETE CASCADE;
ALTER TABLE `User` ADD CONSTRAINT FKUser707408 FOREIGN KEY (avatarImageId) REFERENCES Image (id) ON DELETE CASCADE;
ALTER TABLE FollowedPeople ADD CONSTRAINT FKFollowedPe869855 FOREIGN KEY (followedUserId) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE FollowedPeople ADD CONSTRAINT FKFollowedPe675112 FOREIGN KEY (Userid) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE Comments ADD CONSTRAINT FKComments162338 FOREIGN KEY (parentPostID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE Comments ADD CONSTRAINT FKComments822284 FOREIGN KEY (commentID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE Post ADD CONSTRAINT FKPost991362 FOREIGN KEY (postID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE PostReactions ADD CONSTRAINT FKPostReacti440057 FOREIGN KEY (ReactionId) REFERENCES Reaction (id) ON DELETE CASCADE;
ALTER TABLE Friends ADD CONSTRAINT FKFriends870935 FOREIGN KEY (friend2Id) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE Friends ADD CONSTRAINT FKFriends871896 FOREIGN KEY (friend1Id) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE FollowedTopics ADD CONSTRAINT FKFollowedTo6820 FOREIGN KEY (Topicid) REFERENCES Topic (id) ON DELETE CASCADE;
ALTER TABLE FollowedTopics ADD CONSTRAINT FKFollowedTo900375 FOREIGN KEY (Userid) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE Topic ADD CONSTRAINT FKTopic871983 FOREIGN KEY (parentTopicID) REFERENCES Topic (id) ON DELETE CASCADE;
ALTER TABLE PostTopic ADD CONSTRAINT FKPostTopic597321 FOREIGN KEY (topicid) REFERENCES Topic (id) ON DELETE CASCADE;
ALTER TABLE PostTopic ADD CONSTRAINT FKPostTopic819424 FOREIGN KEY (postID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE PostReactions ADD CONSTRAINT FKPostReacti941606 FOREIGN KEY (reactorID) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE PostReactions ADD CONSTRAINT FKPostReacti625342 FOREIGN KEY (postID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE PostLocations ADD CONSTRAINT FKPostLocati658609 FOREIGN KEY (locationID) REFERENCES Location (locationID) ON DELETE CASCADE;
ALTER TABLE PostLocations ADD CONSTRAINT FKPostLocati299636 FOREIGN KEY (PostID) REFERENCES PostIDs (postID) ON DELETE CASCADE;
ALTER TABLE TaggedPeople ADD CONSTRAINT FKTaggedPeop963559 FOREIGN KEY (userID) REFERENCES `User` (id) ON DELETE CASCADE;
ALTER TABLE TaggedPeople ADD CONSTRAINT FKTaggedPeop66136 FOREIGN KEY (postID) REFERENCES PostIDs (postID) ON DELETE CASCADE;

ALTER TABLE GroupsAdmins ADD CONSTRAINT FKGroupsAdmi712 FOREIGN KEY (Userid) REFERENCES `User` (id);
ALTER TABLE GroupsAdmins ADD CONSTRAINT FKGroupsAdmi964431 FOREIGN KEY (GroupId) REFERENCES `Groups` (id);
ALTER TABLE GroupMembers ADD CONSTRAINT FKGroupMembe991944 FOREIGN KEY (addedByUserId, Groupid) REFERENCES GroupsAdmins (Userid, GroupId);

CREATE INDEX postKey ON Post(postId, authorId);
CREATE INDEX postKey1 ON PostTopic(postId, topicId);

ALTER TABLE FollowedGroupsNotifications ADD constraint FollowKey1 FOREIGN KEY (postId, Groupid) REFERENCES Post(postId, authorId) ON DELETE CASCADE;
ALTER TABLE FollowedTopicsNotifications ADD constraint FollowKey2 FOREIGN KEY (postId, FollowedTopicId) REFERENCES PostTopic(postId, topicId) ON DELETE CASCADE;
ALTER TABLE FollowedPeopleNotifications ADD constraint FollowKey3 FOREIGN KEY (postId, followedUserId) REFERENCES Post(postId, authorId) ON DELETE CASCADE;
ALTER TABLE MembershipRequests ADD CONSTRAINT FKMembership657878 FOREIGN KEY (Groupid) REFERENCES `Groups` (id);
ALTER TABLE MembershipRequests ADD CONSTRAINT FKMembership305281 FOREIGN KEY (UserId) REFERENCES `User` (id);
