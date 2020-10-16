import React, { Component } from "react";
import logo from "../logo.svg";
import "../stylesheets/Header.css";

class Header extends Component {
	navTo(uri) {
		window.location.href = window.location.origin + uri;
	}

	render() {
		return (
			<div className="header" style={{ backgroundColor: "#222" }}>
				<div className="App-header">
					<h1
						onClick={() => {
							this.navTo("");
						}}
					>
						Udacitrivia
					</h1>
					<h2
						onClick={() => {
							this.navTo("");
						}}
					>
						List
					</h2>
					<h2
						onClick={() => {
							this.navTo("/questions/add");
						}}
					>
						Add Question
					</h2>
					<h2
						onClick={() => {
							this.navTo("/categories/add");
						}}
					>
						Add Category
					</h2>
					<h2
						onClick={() => {
							this.navTo("/play");
						}}
					>
						Play
					</h2>
				</div>
				{!this.props.logged ? (
					<div className="login-header ">
						<h2
							style={{ marginRight: "2rem" }}
							onClick={() => {
								this.navTo("/login");
							}}
						>
							Login
						</h2>
						<h2
							onClick={() => {
								this.navTo("/register");
							}}
						>
							Register
						</h2>
					</div>
				) : (
					<div style={{ display: "flex", marginRight: "2rem" }}>
						<h2
							style={{ marginRight: "2rem" }}
							onClick={() => {
								this.props.logout();
							}}
						>
							Logout
						</h2>
						<h2
							onClick={() => {
								this.navTo("/profile");
							}}
						>
							{this.props.username}
						</h2>
					</div>
				)}
			</div>
		);
	}
}

export default Header;
