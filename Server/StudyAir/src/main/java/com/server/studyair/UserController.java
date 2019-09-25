package com.server.studyair;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/user")
public class UserController {

	@Autowired
	private UserRepository repo;
	
	@PostMapping("/newUser") 
	public ResponseEntity<String> newUser(@RequestBody User user){
		System.out.println("Inne!");
		if(user.getUsername() == null|| user.getPassword() == null || user.getEmail() == null) {
			return new ResponseEntity<String>("One of the fields is missing", HttpStatus.BAD_REQUEST);
		}
		else {
			user.setConnectedSystems(null);
			repo.save(user);
			System.out.println("New item saved to MongoDB: " + user);
			return new ResponseEntity<String>("Userinformation loaded into database succesfully", HttpStatus.OK);	
		}
	}
	
	@GetMapping("/addSystem")
	public ResponseEntity<String> addSystem(@RequestParam(value= "system") String system, @RequestParam(value= "username") String username) {
		User user = repo.findByUsername(username);
		if(user.getConnectedSystems() == null) {
			List<String> connectedSystems = new ArrayList<String>();
			user.setConnectedSystems(connectedSystems);
			user.addSystem(system);
			System.out.println("if");
		}
		else {
			user.addSystem(system);
			System.out.println("else");
		}
		repo.save(user);
		System.out.println(user.getConnectedSystems());
		return new ResponseEntity<String>("System succesfully added to user", HttpStatus.OK);
	}
}
