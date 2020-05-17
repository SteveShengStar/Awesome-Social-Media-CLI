import click
import click_repl
import mysql.connector
from click_repl import register_repl
import uuid

#Global variables
userId = None
cnx = None

@click.group()
def cli():
    pass

def missing_user_err():
    click.echo(
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n" + 
        " You must log in first. Please invoke 'signin' or 'signingroup' to log in \n" +
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n"
    )

@cli.command()
def exit():
    # tear down db connections and exit
    cnx.close()
    click_repl.exit()

#@cli.command are the frontend commands, non @cli.command are the APIs
#User login
@cli.command()
def signin():
    displayName = click.prompt(click.style('Please enter your display name', fg='green'), type=str)
    displayNameSearch(displayName)

    global userId 
    userId = click.prompt(click.style('Please select your id', fg='green'), type=str)
    userId = userId.strip()
    userIdSearch(userId)

#Group admin login
@cli.command()
def signinGroup():
    showAllGroups()
    
    groupId = click.prompt(click.style('Please enter group id', fg='green'), type=str)
    while not groupExists(groupId):
        groupId = click.prompt(click.style('Group does not exists, please enter a valid group id', fg='green'), type=str)

    global userId 
    userId = groupId

    click.secho("You're signed", fg="blue")

@cli.command()
def friendRequestsCreatedByMe():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor(buffered=True)
            query = '''(SELECT friend2Id, `User`.first_name, `User`.last_name FROM Friends 
                    LEFT JOIN `User` ON `User`.id = Friends.friend2Id 
                    WHERE friend1Id = "%s" AND statusPending = 1)
                    ''' %(userId)
            
            cursor.execute(query)
            for (friendId, firstname, lastname) in cursor:
                click.secho()
                click.secho("Friend Id: %s" %(friendId), fg="white")
                click.secho("Friend Name: %s" %(firstname + ", " + lastname), fg="white")
            click.secho()
            cursor.close()
    else:
        missing_user_err();

def showFriends():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor(buffered=True)
            query = '''(SELECT friend2Id, `User`.first_name, `User`.last_name FROM Friends 
                    LEFT JOIN `User` ON `User`.id = Friends.friend2Id 
                    WHERE friend1Id = "%s" AND statusPending = 0) UNION 
                    (SELECT friend1Id, `User`.first_name, `User`.last_name FROM Friends 
                    LEFT JOIN `User` ON `User`.id = Friends.friend1Id 
                    WHERE friend2Id = "%s" AND statusPending = 0)
                    ''' %(userId, userId)
            
            cursor.execute(query)
            for (friendId, firstname, lastname) in cursor:
                click.secho()
                click.secho("Friend Id: %s" %(friendId), fg="white")
                click.secho("Friend Name: %s" %(firstname + ", " + lastname), fg="white")
            click.secho()
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def seeFriends():
    showFriends()

@cli.command()
def addFriend(): 
    if (userId):
        if cnx is not None:
            # TODO: Test this
            # TODO: Fix the display names to match first names
            response = click.prompt(click.style("Do you want to search up a person by display name (y/n)? ", fg='green'), type=str)
            if (response in ('Y', 'y')):
                displayName = click.prompt(click.style('Please enter a display name ', fg='green'), type=str)
                displayNameSearch(displayName)

            cursor = cnx.cursor(buffered=True)
            newFriendId = click.prompt(click.style("Enter the ID of the Person you want to friend " , fg='green'), type=str)
            newFriendId = newFriendId.strip()
            try: 
                if (newFriendId == userId):
                    click.secho("Error: you cannot friend yourself.", fg="red")
                else:
                    query = '''SELECT * FROM Friends WHERE 
                            (friend1Id = "%s" AND friend2Id = "%s") \
                            OR (friend1Id = "%s" AND friend2Id = "%s")''' %(userId, newFriendId, newFriendId, userId)
                    cursor.execute(query)

                    if cursor.rowcount == 0:
                        query = "INSERT INTO Friends VALUES('%s', '%s', '%s', NULL, 1);" %(str(uuid.uuid4()), userId, newFriendId)
                        cursor.execute(query)

                        cnx.commit()
                        click.secho("Success! You sent a friend request to %s " %(newFriendId), fg='blue')
                    else:
                        click.secho("Error: Either friend request already sent or you 2 are friends already.", fg='red')
            except:
                click.secho("Error! Friend request not successfully sent. Maybe you already sent one before.", fg='red')
                cnx.rollback()

            cursor.close()
    else:
        missing_user_err();

@cli.command()
def acceptFriendRequests():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()
            query = 'SELECT friend1Id, `User`.first_name, `User`.last_name FROM Friends LEFT JOIN `User` ON `User`.id = Friends.friend1Id WHERE friend2Id = "%s" AND statusPending = 1;' %(userId)
            cursor.execute(query)


            click.secho("List of all pending friend requests.", fg='white')
            for (friendId, firstname, lastname) in cursor:
                click.secho()
                click.secho("Friend ID: %s" %(friendId), fg='white')
                click.secho("Friend Name: %s" %(firstname + ", " + lastname), fg='white')
            

            click.secho()
            newFriendId = click.prompt(click.style("ID of the person whose friend request you want to accept ", fg='green'), type=str)
            newFriendId = newFriendId.strip()
            try: 
                query = 'UPDATE Friends SET statusPending = 0, dateFriended = NOW() WHERE friend2Id = "%s" AND friend1Id = "%s" AND statusPending = 1 AND dateFriended IS NULL;' %(userId, newFriendId)
                cursor.execute(query)

                if cursor.rowcount > 0:
                    cnx.commit()
                    click.secho("Successfully added a new friend.", fg="blue")
                else:
                    cnx.rollback()
                    click.secho("Error: no corresponding friend request was found." , fg="red")
            except e:
                print(e)
                click.secho("Error: Failed to accept freind request.", fg="red")
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def deleteFriend():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()

            response = click.prompt(click.style("Do you want to see your friend list (y/n)? ", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFriends()
            friendToRemove = click.prompt(click.style("User ID of the friend you want to remove ", fg='green'), type=str)
            friendToRemove = friendToRemove.strip()

            try:
                query = '''DELETE FROM Friends 
                            WHERE (friend1Id = "%s" AND friend2Id = "%s") 
                            OR (friend1Id = "%s" AND friend2Id = "%s")''' %(userId, friendToRemove, friendToRemove, userId)
                cursor.execute(query)

                if cursor.rowcount > 0:
                    cnx.commit()
                    click.secho("Success! Friend was removed.", fg="blue")
                else:
                    cnx.rollback()
                    click.secho("Error: check that the friend ID you specified is valid.", fg="red")
            except:
                click.secho("Error: Unable to remove friend. Double-check that the Friend ID was correctly specified.", fg="red")
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def register():
    global userId 
    userId = str(uuid.uuid4())
    firstName = click.prompt(click.style('Please enter your first name', fg='green'), type=str)
    lastName = click.prompt(click.style('Please enter your last name', fg='green'), type=str)
    displayName = click.prompt(click.style('Please enter your display name', fg='green'), type=str)
    email = click.prompt(click.style('Please enter your email', fg='green'), type=str)
    bio = click.prompt(click.style('Please enter your bio', fg='green'), type=str)
    birthYear = click.prompt(click.style('Please enter your birth year', fg='green'), type=click.IntRange(0, 2999))
    birthMonth = click.prompt(click.style('Please enter your birth month', fg='green'), type=click.IntRange(1, 12))
    birthDate = click.prompt(click.style('Please enter your birth date', fg='green'), type=click.IntRange(1, 31))
    birthday = "%i-%i-%i"%(birthYear, birthMonth, birthDate)

    cursor = cnx.cursor(buffered=True)

    query1 = "INSERT INTO projecttest.Party (id) VALUES ('%s')" %(userId)
    cursor.execute(query1)

    query2 = """
    INSERT INTO projecttest.User (id, first_name, last_name, display_name, email, bio, birthday, avatarImageId) 
    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", NULL);
    """%(userId, firstName, lastName, displayName, email, bio, birthday)
    cursor.execute(query2)

    cnx.commit()
    cursor.close()

    userIdSearch(userId)

@cli.command()
def myPosts():
    showPostsOfAnUser(userId)

@cli.command()
def showTopics():
    cursor = cnx.cursor(buffered=True)
    query = "SELECT displayName FROM projecttest.Topic;"
    cursor.execute(query)

    for (index, displayName) in enumerate(cursor):
        click.echo("%s: %s \n"%(index, displayName[0]))

    cursor.close()

@cli.command()
def newPost():
    if (userId is not None):
        text = click.prompt(click.style('Please enter post body', fg='green'), type=str)
        topic = click.prompt(click.style('Please enter post topic', fg='green'), type=str)
        insertNewPost(userId, text, topic)
    else:
        click.secho("Please type signin to sign in first", fg='red')

@cli.command()
def deletePost():
    if (userId is not None):
        postId = click.prompt(click.style('Please enter post id', fg='green'), type=str)
        if (postExists(postId)):
            deleteUserPost(userId, postId)
        else:
            click.secho("Post not found, please supply the correct post id", fg='red')
    else:
        click.secho("Please type signin to sign in first", fg='red')

@cli.command()
def readPost():
    postId = click.prompt(click.style("Please enter the post id", fg='green'), type=str)

    if (postExists(postId)):
        showPost(postId)
        showReactionsOfAnPost(postId)
        showCommentsOfAnPost(postId)
    else:
        click.secho("Post not found, please supply the correct post id", fg='red')

@cli.command()
def reactPost():
    if (userId is not None):
        postId = click.prompt(click.style("Please enter the post id", fg='green'), type=str)
        if (postExists(postId)):
            reactId = click.prompt(click.style(showAvailbleReaction(), fg='green'), type=click.IntRange(1, 5))
            
            query = """
            INSERT INTO projecttest.PostReactions (postID, reactorID, ReactionId, dateCreated, seenByUser) 
            VALUES ("%s", "%s", "%s", CURRENT_TIMESTAMP(), NULL);	
            """%(postId, userId, reactId)

            cursor = cnx.cursor(buffered=True)
            cursor.execute(query)
            cnx.commit()
            cursor.close()

            showEntirePost(postId)
        else:
            click.secho("Post not found, please supply the correct post id", fg='red')
    
    else:
        click.secho("Please type signin to sign in first", fg='red')

@cli.command()
def comment():
    if (userId is not None):
        commentId = str(uuid.uuid4())
        postId = click.prompt(click.style("Please enter the post id", fg='green'), type=str)
        if (postExists(postId)):
            comment = click.prompt(click.style("Please enter your comment", fg='green'), type=str)
            cursor = cnx.cursor(buffered=True)

            #This is nessary as PostIDs contains commentId and postId, but PostIDs table should be renamed in future.
            query1 = "INSERT INTO projecttest.PostIDs(postID) VALUES ('%s')"%(commentId)
            cursor.execute(query1)

            query2 = """
            INSERT INTO projecttest.Comments (commentID, authorID, parentPostID, text, dateCreated, readByPoster) 
            VALUES ("%s", "%s", "%s", "%s", CURRENT_TIMESTAMP(), 0);
            """%(commentId, userId, postId, comment)
            cursor.execute(query2)

            cnx.commit()
            cursor.close()

            showEntirePost(postId)
        else:
            click.secho("Post not found, please supply the correct post id", fg='red')

    else:
        click.secho("Please type signin to sign in first", fg='red')

def showAvailbleReaction(): 
    cursor = cnx.cursor(buffered=True)
    query = "SELECT id, displayName FROM projecttest.Reaction;"

    cursor.execute(query)

    prompt = "Please enter reaction \n"
    for (id, displayName) in cursor:
        prompt += "%s. %s \n"%(id, displayName)

    cursor.close()

    return prompt

def postExists(postId):
    cursor = cnx.cursor(buffered=True)
    query = "SELECT * FROM projecttest.Post where postID = '%s';"%(postId)
    
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()

    return row is not None

def insertNewPost(user_id, text, postTopic):
    cursor = cnx.cursor(buffered=True)
    postId = str(uuid.uuid4())

    query1 = """
    INSERT INTO projecttest.PostIDs (postID) 
    VALUES ("%s");	
    """%(postId)

    query2 = """
    INSERT INTO projecttest.Post (postID, authorID, `text`, datePosted) 
    VALUES ("%s", "%s", "%s", CURRENT_TIMESTAMP());
    """%(postId, user_id, text)

    topicId = findTopicID(postTopic)
    query3 = """
    INSERT INTO projecttest.PostTopic (postID, topicID) 
    VALUES ("%s", "%s");	
    """%(postId, topicId)

    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)

    cnx.commit()

    query = "SELECT userId, followedUserId FROM FollowedPeople WHERE followedUserId = '%s'; " %(user_id)
    cursor.execute(query)
    followedUserRecord = cursor.fetchall()
    for (userId, followedUserId) in followedUserRecord:
        query = "INSERT INTO FollowedPeopleNotifications VALUES ('%s', '%s', '%s', 0);" %(userId, followedUserId, postId)
        #print(query)
        cursor.execute(query)
    cnx.commit()

    query = "SELECT userId, groupId FROM FollowedGroups WHERE GroupId = '%s'; " %(user_id)
    cursor.execute(query)
    followedGroupRecord = cursor.fetchall()
    for (userId, groupId) in followedGroupRecord:
        query = "INSERT INTO FollowedGroupsNotifications VALUES ('%s', '%s', '%s', 0);" %(userId, groupId, postId)
        #print(query)
        cursor.execute(query)
    cnx.commit()

    query = "SELECT userId, topicId FROM FollowedTopics WHERE topicId = '%s';" %(topicId)
    cursor.execute(query)
    followedTopicRecord = cursor.fetchall()
    for (userId, topicId) in followedTopicRecord:
        query = "INSERT INTO FollowedTopicsNotifications VALUES ('%s', '%s', '%s', 0);" %(userId, topicId, postId)
        #print(query)
        cursor.execute(query)
    cnx.commit()

    cursor.close()

    showEntirePost(postId)

def findTopicID(postTopic):
    cursor = cnx.cursor(buffered=True)

    query = "SELECT id FROM projecttest.Topic where displayName = '%s';" %(postTopic)

    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()

    if row:
        return row[0]
    else:
        return (createNewTopic(postTopic))
    
def createNewTopic(topicName):
    if (userId is not None):
        topicId = str(uuid.uuid4())
        cursor = cnx.cursor(buffered=True)

        query = """
        INSERT INTO projecttest.Topic (id, displayName, parentTopicID, topicCreatorId, description, dateCreated) 
        VALUES ("%s", "%s", NULL, "%s", "", CURRENT_TIMESTAMP());
        """%(topicId, topicName, userId)

        cursor.execute(query)
        cnx.commit()
        cursor.close()

        return topicId

    else:
        click.secho("Please type signin to sign in first", fg='red')

def deleteUserPost(user_id, postId):
    cursor = cnx.cursor(buffered=True)

    query1 = """
    DELETE FROM projecttest.Post where postID = "%s" and authorID = "%s";
    """%(postId, user_id)

    query2 = """
    DELETE FROM projecttest.PostTopic where postID = "%s";
    """%(postId)

    query3 = """
    DELETE FROM projecttest.Comments where parentPostID = "%s"
    """%(postId)

    query4 = """
    DELETE FROM projecttest.PostReactions where postID = "%s"
    """%(postId)

    query5 = """
    DELETE FROM projecttest.PostIDs where postID = "%s";
    """%(postId)

    try:
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        cursor.execute(query4)
        cursor.execute(query5)
        cnx.commit()

        click.secho("Success! postId: %s deleted" %(postId), fg='blue')
    
    except mysql.connector.errors.IntegrityError: 
        click.secho("Error postId: %s can not be delete" %(postId), fg='red');
        cnx.rollback()

    cursor.close()

def showFollowedTopics():
    if (userId):
        if cnx is not None:

            cursor = cnx.cursor()
            query = "SELECT topicId, displayName FROM projecttest.FollowedTopics LEFT JOIN Topic ON Topic.id = FollowedTopics.topicId where FollowedTopics.UserId = '%s' ORDER BY TopicId asc;" %(userId)
            cursor.execute(query)

            click.echo("\n")
            for (topicId, displayName) in cursor:
                click.secho("Topic ID: %s " %(topicId), fg='white')
                click.secho("Topic Name: %s \n" %(displayName), fg='white')
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def showMyFollowedTopics():
    showFollowedTopics()

@cli.command()
def followTopic():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()
            response = click.prompt(click.style("Show a list of topics and their Topic IDs (y/n)? ", fg='green'), type=str)
            
            if (response in ("y", "Y")):

                query = "SELECT id, displayName from Topic ORDER BY id asc;"
                cursor.execute(query)
                click.secho("topicId, topicName", fg='white')

                for (topicId, displayName) in cursor:
                    click.secho("%s, %s" %(topicId, displayName), fg='white')

            topicId = click.prompt(click.style("Enter the ID of the topic you want to follow ", fg='green'), type=str)
            topicId = topicId.strip()

            query = "INSERT INTO FollowedTopics VALUES('%s', '%s', NOW());" %(userId, topicId)
            try: 
                cursor.execute(query)
                cnx.commit()

                click.secho("Success! You are now following %s." %(topicId), fg='blue')
            except mysql.connector.errors.IntegrityError: 
                click.secho("Error: Could not add %s to your followed topics list. You may already be following it." %(topicId), fg='red');
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def followPerson():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("Do you want to search up a person by display name (y/n)? ", fg='green'), type=str)
            if (response in ('Y', 'y')):
                displayName = click.prompt(click.style('Please enter a display name ', fg='green'), type=str)
                displayNameSearch(displayName)
            
            followedUserId = click.prompt(click.style("Enter the ID of the user you want to follow ", fg='green'), type=str)
            followedUserId = followedUserId.strip()

            query = "INSERT INTO FollowedPeople VALUES('%s', '%s', NOW());" %(userId, followedUserId)
            try: 
                cursor = cnx.cursor()
                cursor.execute(query)
                cnx.commit()
                click.secho("Success! You are now following %s." %(followedUserId), fg='blue')
            except mysql.connector.errors.IntegrityError: 
                click.secho("Error: Could not add %s to your followed users list. You may already be following him/her." %(followedUserId), fg='red');
                cnx.rollback()
            
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def unfollowTopic():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("Show a list of topics you are following (y/n)? ", fg='green'), type=str)
            
            if (response in ("y", "Y")):
                showFollowedTopics()

            cursor = cnx.cursor()
            topicId = click.prompt(click.style("Enter the ID of the topic you want to unfollow ", fg='green'), type=str)
            topicId = topicId.strip()
            try:
                query = "DELETE FROM FollowedTopics WHERE userId = '%s' AND topicId = '%s'" %(userId, topicId)
                cursor.execute(query)
                cnx.commit()
                
                click.secho("Success! You have unfollowed %s." %(topicId), fg='blue')
            except: 
                click.secho("Error: something went wrong. Topic %s may not be in your followed list." %(topicId), fg='red');
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();

# TODO: Test this
def showFollowedPeople():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT followedUserId, `User`.first_name,`User`.last_name from FollowedPeople AS FP LEFT JOIN `User` ON `User`.id = FP.followedUserId WHERE FP.Userid = '%s';" %(userId)
            cursor.execute(query)
            
            click.secho("List of users you are currently following: ", fg="white")
            for (followedUserId, firstname, lastname) in cursor:
                click.secho()
                click.secho("User Id: %s" %(followedUserId), fg="white")
                click.secho("User Name: %s" %(firstname + ", " + lastname), fg="white")

            click.secho()
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def unfollowPerson():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("Display a list of people you are following (y/n)? ", fg='green'), type=str)
            
            if (response in ("y", "Y")):
                showFollowedPeople()
            
            try:
                cursor = cnx.cursor()
                followedUserId = click.prompt(click.style("Enter the ID of the user you want to unfollow ", fg='green'), type=str)
                followedUserId = followedUserId.strip()

                query = "DELETE FROM FollowedPeople WHERE userId = '%s' AND followedUserId = '%s';" %(userId, followedUserId)
                cursor.execute(query)
                cnx.commit()
                
                click.secho("Success! You have unfollowed %s." %(followedUserId), fg='blue')
            except: 
                click.secho("Error: something went wrong. User %s may not be in your followed list." %(followedUserId), fg='red');
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();


def showFollowedGroups():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT groupId, name FROM projecttest.FollowedGroups LEFT JOIN `Groups` ON `Groups`.id = FollowedGroups.groupId where FollowedGroups.UserId = '%s' ORDER BY GroupId asc;" %(userId)
            cursor.execute(query)

            click.echo("\n")
            for (groupId, displayName) in cursor:
                click.secho("Group ID: %s " %(groupId), fg='white')
                click.secho("Group Name: %s \n" %(displayName), fg='white')
            cursor.close()
    else:
        missing_user_err();

@cli.command()
def showMyFollowedGroups():
    showFollowedGroups()

def groupExists(groupId):
    cursor = cnx.cursor()
    query = "SELECT * FROM projecttest.Groups where id = %s;"%(groupId)

    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()

    return row is not None

def showAllGroups():
    
    response = click.prompt(click.style("Show a list of groups and their Group IDs (y/n)? ", fg='green'), type=str)

    if (response in ("y", "Y")):
        cursor = cnx.cursor()
        query = "SELECT id, name from `Groups` ORDER BY id asc;"
        cursor.execute(query)
        click.secho()
        click.secho("groupId, groupName", fg='white')

        for (groupId, groupName) in cursor:
            click.secho("%s, %s" %(groupId, groupName), fg='white')
        click.secho()
        cursor.close()

@cli.command()
def showAllGroupsCmd():
    showAllGroups()

@cli.command()
def followGroup():
    if (userId):
        if cnx is not None:
            showAllGroups()

            groupId = click.prompt(click.style("Enter the ID of the group you want to follow ", fg='green'), type=str)
            groupId = groupId.strip()
            query = "INSERT INTO FollowedGroups VALUES('%s', '%s', NOW());" %(userId, groupId)
            try:
                cursor = cnx.cursor()
                cursor.execute(query)
                cnx.commit()

                click.secho("Success! You are now following %s." %(groupId), fg='blue')
            except mysql.connector.errors.IntegrityError: 
                click.secho("Error: Could not add %s to your followed groups list. You may already be following it." %(groupId), fg='red');
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();


@cli.command() #TODO: Handle the corner case -- Group is actually not followed initially
def unfollowGroup():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("Show a list of groups you are following (y/n)? ", fg='green'), type=str)
            
            if (response in ("y", "Y")):
                showFollowedGroups()

            cursor = cnx.cursor()
            groupId = click.prompt(click.style("Enter the ID of the group you want to unfollow ", fg='green'), type=str)
            groupId = groupId.strip()
            try:
                query = "DELETE FROM FollowedGroups WHERE userId = '%s' AND groupId = '%s'" %(userId, groupId)
                cursor.execute(query)
                cnx.commit()
                
                click.secho("Success! You have unfollowed %s." %(groupId), fg='blue')
            except: 
                click.secho("Error: something went wrong. Group %s may not be in your followed list." %(groupId), fg='red');
                cnx.rollback()
            cursor.close()
    else:
        missing_user_err();

@cli.command() #TODO: Take care of the image/logo ID.
def createGroup():
    if (userId):
        cursor = cnx.cursor()
        groupName = click.prompt(click.style("What is the Group Name? ", fg='green'), type=str)
        groupDescription = click.prompt(click.style("Give a short description of the Group ", fg='green'), type=str)


        try:
            newGroupId = str(uuid.uuid4())
            query = "INSERT INTO Party VALUES('%s');" %(newGroupId);
            cursor.execute(query)

            query = "INSERT INTO `Groups` VALUES('%s', '%s', '%s', NOW(), '%s', NULL);" %(newGroupId, groupName, groupDescription, userId)
            cursor.execute(query)

            query = "INSERT INTO GroupsAdmins VALUES('%s', '%s');" %(userId, newGroupId)
            cursor.execute(query)

            query = "INSERT INTO GroupMembers VALUES('%s', '%s', NOW(), NULL);" %(userId, newGroupId)
            cursor.execute(query)

            cnx.commit()
            click.secho("Successfully created a new Group.", fg='blue')
        except:
            click.secho("Error: Failed to add new group %s" %(groupName), fg='red')
            cnx.rollback()

        cursor.close()
    else:
        missing_user_err()

@cli.command()
def showGroupsWhereIAmMember():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()

            query = "SELECT GroupId, `Groups`.`name`, `User`.first_name, `User`.last_name FROM GroupMembers LEFT JOIN `User` ON GroupMembers.addedByUserId = `User`.id LEFT JOIN `Groups` ON `Groups`.id = GroupMembers.Groupid WHERE Userid = '%s';" %(userId)
            cursor.execute(query)

            click.secho("You are a member of these groups: ", fg="white")
            for (groupId, groupName, addedByUserFirstname, addedByUserLastname) in cursor:
                click.secho()
                click.secho("Group ID: %s" %(groupId), fg="white")
                click.secho("Group Name: %s" %(groupName), fg="white")
                click.secho("Name of user who added you: %s" %( (addedByUserFirstname if addedByUserFirstname else "") + ", " + (addedByUserLastname if addedByUserLastname else "") ), fg="white")
            
            click.secho()
            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showGroupsWhereIAmAdmin():
    if (userId):
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT GroupId, `Groups`.`name` FROM GroupsAdmins LEFT JOIN `Groups` ON `Groups`.id = GroupsAdmins.Groupid WHERE Userid = '%s';" %(userId)
            cursor.execute(query)

            click.secho("You are an admin for these groups: ", fg="white")
            for (groupId, groupName) in cursor:
                click.secho()
                click.secho("Group ID: %s" %(groupId), fg="white")
                click.secho("Group Name: %s" %(groupId), fg="white")
            
            click.secho()
            cursor.close()
    else:
        missing_user_err()

@cli.command()
def requestGroupMembership():
    if (userId):
        showAllGroups()

        cursor = cnx.cursor()
        groupId = click.prompt(click.style("Id of the group you want to request access to: ", fg='green'), type=str);
        groupId = groupId.strip()
        query = "SELECT groupId from GroupMembers WHERE userId = '%s'" %(userId)
        try: 
            cursor.execute(query)

            shouldSendNotification = True
            for (candidateGroupId) in cursor:
                if groupId == candidateGroupId[0]:
                    shouldSendNotification = False
                    break

            if shouldSendNotification:
                query = "INSERT INTO MembershipRequests VALUES('%s', '%s', NOW())" %(userId, groupId)
                cursor.execute(query)
                cnx.commit()
                click.secho("Success: Request to join group %s was sent." %(groupId), fg='blue')
            else: 
                click.secho("Error: You are already part of this group.", fg='red')
                cnx.rollback()
        except mysql.connector.errors.IntegrityError:
            click.secho("Error: You may have already sent a request.", fg='red')
            cnx.rollback()
        cursor.close()
    else:
        missing_user_err()

def showPendingRequests():
    if (userId):
        cursor = cnx.cursor()

        click.secho()
        click.secho("List of pending membership requests: ", fg="white")
        click.secho()
        query = '''SELECT `Groups`.id, `Groups`.name, Req.UserId, `User`.first_name, `User`.last_name from MembershipRequests AS Req
                LEFT JOIN GroupsAdmins AS GAdmin USING (Groupid) 
                LEFT JOIN `Groups` ON `Groups`.id = GAdmin.GroupId
                LEFT JOIN `User` ON `User`.id = Req.UserId
                WHERE GAdmin.UserId = "%s";''' %(userId);

        cursor.execute(query)
        for (groupId, groupName, Id, firstName, lastName) in cursor:
            click.secho("Group ID: %s" %(groupId))
            click.secho("Group Name: %s" %(groupName))
            click.secho("Requesting User ID: %s" %(Id))
            click.secho("Requesting User Name: %s" %(firstName + ", " + lastName))
            click.secho()
        click.secho()
        cursor.close()
    else:
        missing_user_err()

@cli.command()
def grantGroupMembership():
    if (userId):
        showPendingRequests()
        cursor = cnx.cursor()

        groupId = click.prompt(click.style("ID of the group you want to add new member to ", fg='green'), type=str)
        groupId = groupId.strip()
        newMemberId = click.prompt(click.style("ID of the new member ", fg='green'), type=str)
        newMemberId = newMemberId.strip()
        try: 
            query = 'DELETE FROM MembershipRequests WHERE userID = "%s" AND groupId = "%s"' %(newMemberId, groupId)
            cursor.execute(query)
            
            query = 'INSERT INTO GroupMembers VALUES("%s", "%s", NOW(), "%s")' %(newMemberId, groupId, userId)
            cursor.execute(query)

            cnx.commit()
            click.secho("Success! New member was added.", fg='blue')
        except e:
            click.secho("Error: Failed to add new member.", fg='red')
            cnx.rollback()
        cursor.close()

def userIdSearch(user_id): 
    cursor = cnx.cursor(buffered=True)

    query = "SELECT first_name, last_name FROM projecttest.User where id = '%s';" %(user_id)
    cursor.execute(query)

    row = cursor.fetchone()

    if (row is not None):
        click.secho("Welcome %s %s, you're signed in"%(row[0], row[1]), fg='blue')
    else:
        click.secho("User Id not found, please sign in again", fg='red')
        userId = None

    cursor.close()   

def displayNameSearch(displayName): 
    cursor = cnx.cursor(buffered=True)

    query = "SELECT id, first_name, last_name, display_name FROM projecttest.User where display_name = '%s';" %(displayName)
    cursor.execute(query)

    for (id, first_name, last_name, display_name) in cursor:
        click.echo(
            "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n" + 
            " id: %s \n first name: %s \n last name: %s \n display name: %s \n"
            %(id, first_name, last_name, display_name) +    
            "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n"            
        )
    cursor.close()

def showPostsOfAnUser(userID):
    if cnx is not None:
        cursor = cnx.cursor(buffered=True)
        query = """
        SELECT projecttest.Post.postID, authorID, text, datePosted, displayName FROM projecttest.Post inner join projecttest.PostTopic on projecttest.Post.postID = projecttest.PostTopic.postID
        inner join projecttest.Topic on projecttest.PostTopic.topicid = projecttest.Topic.id
        where authorId = '%s'         
        """ % userID 

        cursor.execute(query)

        for (postID, authorID, text, datePosted, displayName) in cursor:
            click.secho("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+Post-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n", fg = "blue")
            click.echo(
                " postID: %s \n authorID: %s \n postBody: %s \n topic: %s \n postDate: %s \n"
                %(postID, authorID, text, displayName, datePosted.strftime('%H-%M %m/%d/%Y')))
            showReactionsOfAnPost(postID)
            showCommentsOfAnPost(postID)

    
        cursor.close()

def showEntirePost(postId):
    if postId:
        showPost(postId)
        showReactionsOfAnPost(postId)
        showCommentsOfAnPost(postId)

def showPost(postId):
    cursor = cnx.cursor(buffered=True)
    query = """
    SELECT projecttest.Post.postID, authorID, text, displayName, datePosted FROM projecttest.Post inner join projecttest.PostTopic on projecttest.Post.postID = projecttest.PostTopic.postID
    inner join projecttest.Topic on projecttest.PostTopic.topicid = projecttest.Topic.id
    where projecttest.Post.postID = '%s'         
    """ % postId 
    
    cursor.execute(query)
    row = cursor.fetchone()
    click.secho("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+Post-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n", fg = "blue")
    click.echo(
        " postID: %s \n authorID: %s \n postBody: %s \n topic: %s \n postDate: %s \n"
        %(row[0], row[1], row[2], row[3], row[4].strftime('%H-%M %m/%d/%Y')))

    cnx.commit()

    # detect if authour is a followed group or user
    query = "SELECT UserId FROM FollowedPeople WHERE userId = '%s' AND followedUserId = '%s';" %(userId, row[1].strip())
    cursor.execute(query)
    if cursor.rowcount > 0:
        try:
            query = '''UPDATE FollowedPeopleNotifications SET seenByFollower = 1 
            WHERE userId = "%s" AND followedUserId = "%s" AND postId = "%s"''' %(userId, row[1].strip(), row[0].strip())
            cursor.execute(query)

            cnx.commit()
        except:
            click.secho("Error: failed to update the notification table.", fg="red")
            cnx.rollback()


    query = "SELECT UserId FROM FollowedGroups WHERE userId = '%s' AND groupId = '%s';" %(userId, row[1].strip())
    cursor.execute(query)
    if cursor.rowcount > 0:
        try:
            query = '''UPDATE FollowedGroupsNotifications SET seenByFollower = 1 
            WHERE userId = "%s" AND groupId = "%s" AND postId = "%s"''' %(userId, row[1].strip(), row[0].strip())
            cursor.execute(query)
            cnx.commit()
        except:
            click.secho("Error: failed to update the notification table.", fg="red")
            cnx.rollback()

    query = "SELECT DISTINCT TopicId FROM FollowedTopics INNER JOIN PostTopic USING(TopicId) WHERE userId = '%s' AND postId = '%s';" %(userId, postId)
    cursor.execute(query)
    if cursor.rowcount > 0:
        try:
            allFollowedTopics = cursor.fetchall()
            for (topicId) in allFollowedTopics:
                query = '''UPDATE FollowedTopicsNotifications SET seenByFollower = 1 
                WHERE userId = "%s" AND followedTopicId = "%s" AND postId = "%s";''' %(userId, topicId[0], postId)
                cursor.execute(query)
            cnx.commit()
        except:
            click.secho("Error: failed to update the notification table.", fg="red")
            cnx.rollback()
    cursor.close()

def showReactionsOfAnPost(postId):
    cursor = cnx.cursor(buffered=True)
    reactionSet = ["Like",  "Thumbs Down", "Laugh", "Heart", "Sad"]
    click.secho("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+Reactions-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+", fg = "blue")
    for reaction in reactionSet:
        query = """ SELECT displayName, count(postID) as likeNum FROM projecttest.PostReactions 
        inner join projecttest.Reaction on projecttest.PostReactions.ReactionId = projecttest.Reaction.id
        where postID = "%s" and displayName = "%s";
        """%(postId, reaction)

        cursor.execute(query)
        row = cursor.fetchone()
        if (row[1] > 0):
            click.echo(" %s: %i"%(row[0], row[1]))
    
    cursor.close()

def showCommentsOfAnPost(postId):
    cursor = cnx.cursor(buffered=True)
    click.secho("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+Comments-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+", fg = "blue")

    query = """
    SELECT commentID, authorID, text, projecttest.User.display_name, dateCreated FROM projecttest.Comments
    inner join projecttest.User on projecttest.Comments.authorID = projecttest.User.id 
    where parentPostID = '%s';
    """%(postId)

    cursor.execute(query)
    for (commentID, authorID, text, displayName, dateCreated) in cursor:
        click.echo(""" commentID: %s \n authorID: %s \n comment: %s \n by: %s \n date: %s \n"""
        %(commentID, authorID, text, displayName, dateCreated.strftime('%H-%M %m/%d/%Y')))
    cursor.close()

@cli.command()
def showAllPostsByTopic():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the Topics you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedTopics();

            cursor = cnx.cursor(buffered=True)

            topicId = click.prompt(click.style("Enter the ID of the Topic you are interested in ", fg='green'), type=str)
            topicId = topicId.strip()
            query = '''
            SELECT postID FROM 
            ( SELECT * FROM (
                WITH RECURSIVE topic_specializations (id, displayName, path) AS
                (
                    SELECT id, displayName, CAST(id AS CHAR(400))
                        FROM Topic
                        WHERE id = '%s'
                    UNION ALL
                    SELECT t.id, t.displayName, CONCAT(tspec.path, ',', t.id)
                        FROM topic_specializations AS tspec JOIN Topic AS t
                        ON tspec.id = t.parentTopicID
                )
                SELECT id, displayName, path FROM topic_specializations ORDER BY path
            ) AS AllFollowed LEFT JOIN PostTopic AS PT ON AllFollowed.id = PT.Topicid ) as temp;
            ''' %(topicId)
            cursor.execute(query);
            posts = cursor.fetchall();

            if (len(posts) > 0):
                for postId in posts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no Posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showUnreadPostsByTopic():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the Topics you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedTopics();

            cursor = cnx.cursor(buffered=True)

            followedTopicId = click.prompt(click.style("Enter the ID of the Topic you are interested in ", fg='green'), type=str)
            followedTopicId = followedTopicId.strip()
            query = '''SELECT postId from FollowedTopicsNotifications 
                        WHERE Userid = "%s" AND FollowedTopicId = "%s" AND seenByFollower = 0;''' %(userId, followedTopicId)
            cursor.execute(query);
            unreadPosts = cursor.fetchall();

            if (len(unreadPosts) > 0):
                for postId in unreadPosts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no Unseen Posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showAllPostsByUser():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the People you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedPeople();

            cursor = cnx.cursor(buffered=True)

            visitedUserId = click.prompt(click.style("Enter the ID of the Person whose posts you want to see ", fg='green'), type=str)
            visitedUserId = visitedUserId.strip()
            query = '''SELECT postId from Post 
                        WHERE authorId = "%s";''' %(visitedUserId)
            cursor.execute(query);
            posts = cursor.fetchall();

            if (len(posts) > 0):
                for postId in posts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no Posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showUnreadPostsByUser():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the People you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedPeople();

            cursor = cnx.cursor(buffered=True)

            followedUserId = click.prompt(click.style("Enter the ID of the Person whose posts you want to see ", fg='green'), type=str)
            followedUserId = followedUserId.strip()
            query = '''SELECT postId from FollowedPeopleNotifications 
                        WHERE Userid = "%s" AND followedUserId = "%s" AND seenByFollower = 0;''' %(userId, followedUserId)
            cursor.execute(query);
            unreadPosts = cursor.fetchall();

            if (len(unreadPosts) > 0):
                for postId in unreadPosts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no Unseen Posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showAllPostsByGroup():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the Groups you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedGroups();

            cursor = cnx.cursor(buffered=True)

            groupId = click.prompt(click.style("Enter the ID of the Group you are interested in ", fg='green'), type=str)
            groupId = groupId.strip()
            query = '''SELECT postId from Post 
                        WHERE authorId = "%s";''' %(groupId)
            cursor.execute(query);
            posts = cursor.fetchall();

            if (len(posts) > 0):
                for postId in posts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

@cli.command()
def showUnreadPostsByGroup():
    if (userId):
        if cnx is not None:
            response = click.prompt(click.style("List out the Groups you are currently following (y/n)?", fg='green'), type=str)
            if (response in ('Y', 'y')):
                showFollowedGroups();

            cursor = cnx.cursor(buffered=True)

            groupId = click.prompt(click.style("Enter the ID of the Group you are interested in ", fg='green'), type=str)
            groupId = groupId.strip()
            query = '''SELECT postId from FollowedGroupsNotifications 
                        WHERE Userid = "%s" AND Groupid = "%s" AND seenByFollower = 0;''' %(userId, groupId)
            cursor.execute(query);
            unreadPosts = cursor.fetchall();

            if (len(unreadPosts) > 0):
                for postId in unreadPosts:
                    showEntirePost(postId[0]) 
            else:
                click.secho("There are no Unseen Posts to show !", fg='white')

            cursor.close()
    else:
        missing_user_err()

def startDb():
    # establish connection to the db
    global cnx
    cnx = mysql.connector.connect(user='root', password='!1Scholar!',
                              host='127.0.0.1',
                              database='projecttest',
                              auth_plugin='mysql_native_password')

def welcomeMessage():
    click.secho("Welcome, please signin or register", fg='blue')

register_repl(cli)
startDb()
welcomeMessage()
cli()