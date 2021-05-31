/* eslint-disable no-useless-escape */
import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/QuizView.css";

const questionsPerPlay = 5;

class ProfileView extends Component {
	constructor(props) {
		super();
		this.state = {
			quizzes: [],
		};
	}
	saveUserScore = () => {
		$.ajax({
			url: `/users/quizzes`, //TODO: update request URL
			type: "POST",
			headers: {
				"xx-auth-token": this.props.token,
			},
			dataType: "json",
			contentType: "application/json",
			data: JSON.stringify({
				token: this.props.token,
				score: this.state.numCorrect,
				category: this.state.quizCategory,
			}),
			success: (result) => {
				alert("score has been saved successfully");
				return;
			},
			error: (error) => {
				alert("Score saving process failed");
				return;
			},
		});
	};
	componentDidMount() {
		// console.log(localStorage.getItem("xx-auth-token"));
		$.ajax({
			url: `/users/quizzes`, //TODO: update request URL
			type: "GET",
			headers: {
				"xx-auth-token": localStorage.getItem("xx-auth-token"),
			},
			success: (result) => {
				this.setState({ quizzes: result.quizzes });
				return;
			},
			error: (error) => {
				alert("Unable to load categories. Please try your request again");
				return;
			},
		});
	}

	renderUserQuizzes() {
		return (
			<div
				className="quiz-play-holder"
				style={{ width: "90%", marginLeft: "5%" }}
			>
				<div className="category-holder">
					<h2 className="play-category" style={{ marginBottom: "2rem" }}>
						Your Quiz History{" "}
					</h2>

					<div
						style={{
							display: "flex",
							flexWrap: "wrap",
							alignItems: "center",
							justifyContent: "center",
						}}
					>
						{this.state.quizzes.length > 0 ? (
							this.state.quizzes.map((quizz) => {
								return (
									<div
										style={{
											cursor: "pointer",
											marginRight: "1rem",
											marginBottom: "1rem",
											backgroundColor: "#fff",
											boxShadow: "3px 3px 5px 2px rgba(0,0,0,.1)",
											border: "solid 1px rgba(0,0,0,.1)",
											padding: "1rem",
											textAlign: "left",
											width: "300px",
										}}
										key={quizz.id}
										value={quizz.id}
										className="play-category"
									>
										<div style={{ marginBottom: "1rem" }}>
											Category: {quizz.category.type}
										</div>
										<div>Score: {quizz.result}</div>
									</div>
								);
							})
						) : (
							<h2>There is no Quizzes</h2>
						)}
					</div>
				</div>
			</div>
		);
	}

	render() {
		return this.renderUserQuizzes();
	}
}

export default ProfileView;
