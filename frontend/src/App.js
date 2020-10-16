import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import $ from "jquery";
// import logo from './logo.svg';
import "./stylesheets/App.css";
import QuestionForm from "./components/QuestionForm";
import CategoryForm from "./components/CategoryForm";
import UserForm from "./components/UserForm";
import QuestionView from "./components/QuestionView";
import Header from "./components/Header";
import QuizView from "./components/QuizView";
import ProfileView from "./components/ProfileView";

class App extends Component {
	constructor() {
		super();
		this.state = {
			username: "",
			token: localStorage.getItem("xx-auth-token"),
			logged: false,
		};
	}
	componentDidMount() {
		let token = localStorage.getItem("xx-auth-token");
		if (token) {
			$.ajax({
				url: `/users`, //TODO: update request URL
				type: "POST",
				dataType: "json",
				contentType: "application/json",
				data: JSON.stringify({
					token: token,
				}),
				xhrFields: {
					withCredentials: true,
				},
				crossDomain: true,
				success: (result) => {
					this.setState({
						username: result.username,
						token: result.token,
						logged: true,
					});
					return;
				},
				error: (error) => {
					if (error.status === 403) {
						if (this.state.logged) {
							alert(error.responseJSON.error);
						}
						this.setState({ logged: false, username: "", token: "" });
						localStorage.removeItem("xx-auth-token");
						return;
					}

					alert(error.responseJSON.error);

					return;
				},
			});
		}
	}
	logout = () => {
		// since i didnt save the token in the database
		this.setState({ logged: false, token: "", username: "" });
		localStorage.removeItem("xx-auth-token");
		// thats all
	};
	submitUser = (event, username, password, title) => {
		event.preventDefault();
		$.ajax({
			url: `/users${title.toLowerCase()}`, //TODO: update request URL
			type: "POST",
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				username: username,
				password: password,
			}),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {
				this.setState({
					username: result.username,
					token: result.token,
					logged: true,
				});
				localStorage.setItem("xx-auth-token", result.token);

				window.location.href = window.location.origin;
				return;
			},
			error: (error) => {
				if (error.status === 403) {
					if (this.state.logged) {
						alert(error.responseJSON.error);
					}
					this.setState({ logged: false, username: "", token: "" });
					localStorage.removeItem("xx-auth-token");

					return;
				}
				alert(error.responseJSON.message);

				return;
			},
		});
	};
	render() {
		return (
			<div className="App">
				<Header
					path
					logged={this.state.logged}
					username={this.state.username}
					logout={this.logout}
				/>
				<Router>
					<Switch>
						<Route
							path="/"
							exact
							render={(props) => (
								<QuestionView token={this.state.token} {...props} />
							)}
						/>
						<Route
							path="/questions/add"
							render={(props) => (
								<QuestionForm method="POST" title="Add New " {...props} />
							)}
						/>

						<Route
							path="/questions/edit"
							render={(props) => (
								<QuestionForm
									method="PUT"
									title="Edit the selected "
									{...props}
								/>
							)}
						/>
						<Route
							path="/categories/add"
							render={(props) => (
								<CategoryForm
									token={this.state.token}
									method="POST"
									title="Add New "
									{...props}
								/>
							)}
						/>
						<Route
							path="/categories/edit"
							render={(props) => (
								<CategoryForm
									token={this.state.token}
									method="PUT"
									title="Edit the selected "
									{...props}
								/>
							)}
						/>
						<Route
							path="/login"
							render={(props) => (
								<UserForm
									title="Login"
									username={this.state.username}
									logged={this.state.logged}
									token={this.state.token}
									submitUser={this.submitUser}
									{...props}
								/>
							)}
						/>
						<Route
							path="/register"
							render={(props) => (
								<UserForm
									{...props}
									username={this.state.username}
									logged={this.state.logged}
									token={this.state.token}
									title="Register"
									submitUser={this.submitUser}
								/>
							)}
						/>
						<Route
							path="/profile"
							render={(props) => (
								<ProfileView
									{...props}
									username={this.state.username}
									logged={this.state.logged}
									token={this.state.token}
									title="Profile"
								/>
							)}
						/>
						<Route
							path="/play"
							render={(props) => (
								<QuizView {...props} token={this.state.token} />
							)}
						/>
					</Switch>
				</Router>
			</div>
		);
	}
}

export default App;
