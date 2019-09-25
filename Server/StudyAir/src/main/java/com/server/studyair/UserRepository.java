package com.server.studyair;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.query.Param;

public interface UserRepository  extends MongoRepository<User, String> {

    public User findByUsername(@Param("username") String name);
    public User findByEmail(@Param("email") String email);
}
