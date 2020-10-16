import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class QuestionForm extends Component {
	constructor(props) {
		super();
		this.state = {
			question: "",
			answer: "",
			difficulty: 1,
			category: 1,
			rating: 1,
			categories: {},
		};
	}

	componentDidMount() {
		if (this.props.history.location.state) {
			$.ajax({
				url: `/questions/${this.props.history.location.state.questionId}`,
				type: "GET",
				dataType: "json",
				contentType: "application/json",
				xhrFields: {
					withCredentials: true,
				},
				crossDomain: true,
				success: (result) => {
					this.setState({
						question: result.question.question,
						answer: result.question.answer,
						difficulty: result.question.difficulty,
						rating: result.question.rating,
						category: result.question.category.id,
					});
					return;
				},
				error: (error) => {
					alert("Unable to add question. Please try your request again");
					return;
				},
			});
		}
		$.ajax({
			url: `/categories`, //TODO: update request URL
			type: "GET",
			success: (result) => {
				this.setState({ categories: result.categories });
				return;
			},
			error: (error) => {
				alert(
					"Unable to load categories. Please try your request again",
					error
				);
				return;
			},
		});
	}

	submitQuestion = (event) => {
		const method = this.props.method;
		event.preventDefault();
		$.ajax({
			url: `/questions${
				method === "PUT" ? "/" + this.props.location.state.questionId : ""
			}`, //TODO: update request URL
			type: this.props.method,
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				question: this.state.question,
				answer: this.state.answer,
				difficulty: this.state.difficulty,
				rating: this.state.rating,
				category: this.state.category,
			}),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {
				this.setState({
					question: "",
					answer: "",
					difficulty: 1,
					rating: 1,
					category: 1,
				});
				document.getElementById("add-question-form").reset();
				return;
			},
			error: (error) => {
				alert("Unable to add question. Please try your request again");
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
				<h2>{this.props.title} Trivia Question</h2>
				<form
					className="form-view"
					id="add-question-form"
					onSubmit={this.submitQuestion}
				>
					<label>
						Question
						<input
							type="text"
							name="question"
							required
							onChange={this.handleChange}
							value={this.state.question}
						/>
					</label>
					<label>
						Answer
						<input
							type="text"
							name="answer"
							required
							onChange={this.handleChange}
							value={this.state.answer}
						/>
					</label>
					<label>
						Difficulty
						<select
							name="difficulty"
							onChange={this.handleChange}
							value={this.state.difficulty}
						>
							<option value="1">1</option>
							<option value="2">2</option>
							<option value="3">3</option>
							<option value="4">4</option>
							<option value="5">5</option>
						</select>
					</label>
					<label>
						Rating
						<select
							name="rating"
							onChange={this.handleChange}
							value={this.state.rating}
						>
							<option value="1">1</option>
							<option value="2">2</option>
							<option value="3">3</option>
							<option value="4">4</option>
							<option value="5">5</option>
						</select>
					</label>
					<label>
						Category
						{this.state.categories.length > 0 ? (
							<select
								name="category"
								onChange={this.handleChange}
								value={this.state.category}
							>
								{this.state.categories.map(({ id, type }) => {
									return (
										<option key={id} value={id}>
											{type}
										</option>
									);
								})}
							</select>
						) : (
							<h2>There is no categories</h2>
						)}
					</label>
					<input type="submit" className="button" value="Submit" />
				</form>
			</div>
		);
	}
}

export default QuestionForm;
