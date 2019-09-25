package com.server.studyair;

import java.util.List;

import org.springframework.data.annotation.Id;

public class User {

	@Id
    public String id;
	private String username;
	private String password;
	private String email;
	private List<String> connectedSystems;
	
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public List<String> getConnectedSystems() {
		return connectedSystems;
	}
	public void setConnectedSystems(List<String> connectedSystems) {
		this.connectedSystems = connectedSystems;
	}
	
	public void addSystem(String system) {
		connectedSystems.add(system);
	}
	
	public void removeSystem(String system) {
		connectedSystems.remove(system);
	}
	
}
