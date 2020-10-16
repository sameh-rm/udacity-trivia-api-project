import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class CategoryForm extends Component {
	constructor(props) {
		super();
		this.state = {
			type: "",
			image_link: "",
		};
	}

	componentDidMount() {
		if (this.props.history.location.state) {
			$.ajax({
				url: `/categories/${this.props.history.location.state.categoryId}`,
				type: "GET",
				dataType: "json",
				contentType: "application/json",
				xhrFields: {
					withCredentials: true,
				},
				crossDomain: true,
				success: (result) => {
					this.setState({
						type: result.category.type,
						image_link: result.category.image_link,
					});
					return;
				},
				error: (error) => {
					alert(error.responseJSON.message);
					return;
				},
			});
		}
	}

	submitCategory = (event) => {
		const PUT = this.props.method === "PUT";
		event.preventDefault();
		$.ajax({
			url: `/categories${
				PUT ? "/" + this.props.location.state.categoryId : ""
			}`, //TODO: update request URL
			headers: {
				"xx-auth-token": this.props.token,
			},
			type: this.props.method,
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				type: this.state.type,
				image_link: this.state.image_link,
			}),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {
				this.setState({
					type: "",
					image_link: "",
				});
				document.getElementById("add-category-form").reset();
				this.props.history.push("/");
				return;
			},
			error: (error) => {
				alert(error.responseJSON.message);
				return;
			},
		});
	};

	handleChange = (event) => {
		this.setState({ [event.target.name]: event.target.value });
	};

	render() {
		return (
			<div id="add-form">
				<h2>{this.props.title} Category</h2>
				<form
					className="form-view"
					id="add-category-form"
					onSubmit={this.submitCategory}
				>
					<label>
						Category Type
						<input
							type="text"
							name="type"
							required
							onChange={this.handleChange}
							value={this.state.type}
						/>
					</label>
					<label>
						Image Link
						<input
							type="text"
							name="image_link"
							required
							onChange={this.handleChange}
							value={this.state.image_link}
						/>
					</label>

					<input type="submit" className="button" value="Submit" />
				</form>
			</div>
		);
	}
}

export default CategoryForm;
