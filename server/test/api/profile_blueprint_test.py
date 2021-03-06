from server.test import assert_api_error, assert_api_response, assert_api_success
from server.library.util import find
from json import loads

def test_profile_courses_empty(auth_client):
    resp = auth_client.get("/profile/courses")

    with assert_api_response(resp) as data:
        assert len(data["courses"]) == 0

def test_profile_courses(auth_client, user_with_courses):
    resp = auth_client.get("/profile/courses")

    with assert_api_response(resp) as data:
        assert len(data["courses"]) == 5

def test_profile_add_course(auth_client, user, courses, session):
    newCourse = courses[0]
    resp = auth_client.patch("/profile/courses", data={ "course": newCourse.id })
    
    assert_api_success(resp)
    session.refresh(user)
    assert len(user.courses) > 0

def test_profile_add_course_existing(auth_client, user_with_courses, session):
    existingCourse = user_with_courses.courses[0]
    resp = auth_client.patch("/profile/courses", data={ "course": existingCourse.id })

    # This is intended behaviour because if the user already has the
    # course associated, then this request will *always* be a success
    # It's up to the client to notice that the user already has the
    # course associated.
    assert_api_success(resp) 
    session.refresh(user_with_courses)
    assert len(user_with_courses.courses) == 5

def test_profile_delete_course(auth_client, user_with_courses, session):
    existingCourse = user_with_courses.courses[0]
    resp = auth_client.delete("/profile/courses", data={ "course": existingCourse.id })

    assert_api_success(resp)
    session.refresh(user_with_courses)
    assert len(user_with_courses.courses) == 4
    assert not find(user_with_courses.courses, lambda mod: mod.id == existingCourse.id)