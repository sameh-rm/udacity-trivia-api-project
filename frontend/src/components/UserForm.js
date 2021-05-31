import React, { Component } from "react";
import "../stylesheets/FormView.css";

class UserForm extends Component {
	constructor(props) {
		super();
		this.state = {
			username: "",
			password: "",
		};
	}

	componentDidMount() {
		// console.log(this.props.username);
		if (this.props.username) {
			this.props.history.push("/");
		}
	}

	handleChange = (event) => {
		this.setState({ [event.target.name]: event.target.value });
	};

	render() {
		return (
			<div id="add-form">
				<h2>{this.props.title}</h2>
				<form
					className="form-view"
					id="user-form"
					onSubmit={(event) =>
						this.props.submitUser(
							event,
							this.state.username,
							this.state.password,
							`/${this.props.title.toLowerCase()}`
						)
					}
				>
					<label>
						UserName
						<input
							type="text"
							name="username"
							required
							onChange={this.handleChange}
							// value={this.state.type}
						/>
					</label>
					<label>
						Password
						<input
							type="password"
							name="password"
							required
							onChange={this.handleChange}
							// value={this.state.image_link}
						/>
					</label>

					<input type="submit" className="button" value={this.props.title} />
				</form>
			</div>
		);
	}
}

export default UserForm;
